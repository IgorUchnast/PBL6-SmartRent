# app.py (main_service)

from sqlite3 import OperationalError
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS
import time
from extensions import db, jwt
from models import Lightbulb, Property, Reservation, Outlet, Sensor, SensorData
import requests

DOWNLINK_URL = "http://edge_downlink:5000/command"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/smartrent'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

CORS(app)
db.init_app(app)
jwt.init_app(app)

@app.route("/properties", methods=["POST"])
@jwt_required()
def add_property():
    user_id = get_jwt_identity()
    data = request.get_json()
    description = data.get("description")
    price = data.get("price")
    status = data.get("status", "free")
    if not description or price is None:
        return jsonify({"error": "Missing fields"}), 400
    new_property = Property(user_id=user_id, status=status, description=description, price=price)
    db.session.add(new_property)
    db.session.commit()
    return jsonify({"message": "Property added successfully"}), 201

@app.route("/properties/public", methods=["GET"])
def get_all_properties_public():
    properties = Property.query.filter_by(status="Active").all()
    return jsonify([{ "id": prop.id, "status": prop.status, "description": prop.description, "price": prop.price, "name": f"Mieszkanie #{prop.id}" } for prop in properties]), 200

@app.route("/properties", methods=["GET"])
@jwt_required()
def get_user_properties():
    user_id = get_jwt_identity()
    properties = Property.query.filter_by(user_id=user_id).all()
    return jsonify([{ "id": prop.id, "status": prop.status, "description": prop.description, "price": prop.price } for prop in properties]), 200

@app.route("/reservations", methods=["GET"])
@jwt_required()
def get_user_reservations():
    user_id = get_jwt_identity()
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    return jsonify([{ "id": res.id, "property_id": res.property_id, "start_date": res.start_date.isoformat(), "end_date": res.end_date.isoformat(), "status": res.status } for res in reservations]), 200

@app.route("/outlets/<int:outlet_id>/status", methods=["GET"])
def get_outlet_status(outlet_id):
    outlet = Outlet.query.get(outlet_id)
    if not outlet:
        return jsonify({"error": "Outlet not found"}), 404

    def latest(sensor):
        if not sensor:
            return None
        data = SensorData.query.filter_by(sensor_id=sensor.id).order_by(SensorData.timestamp.desc()).first()
        return data.value if data else None

    return jsonify({
        "status": outlet.status,
        "power_consumption": latest(outlet.power_sensor),
        "voltage": latest(outlet.voltage_sensor),
        "amparage": latest(outlet.amperage_sensor),
        "total": latest(outlet.total_sensor)
    }), 200

@app.route("/outlets/<int:outlet_id>/toggle", methods=["POST"])
def toggle_outlet_status(outlet_id):
    outlet = Outlet.query.get(outlet_id)
    if not outlet:
        return jsonify({"error": "Outlet not found"}), 404
    cmd = "turn_off_outlet" if outlet.status == "on" else "turn_on_outlet"
    outlet.status = "off" if outlet.status == "on" else "on"
    try:
        response = requests.post(DOWNLINK_URL, json={"methodName": "execute", "payload": {"command": cmd}})
        if response.status_code != 200:
            return jsonify({"error": "Failed to toggle outlet status"}), 500
    except requests.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500
    db.session.commit()
    return jsonify({"message": "Outlet status updated", "status": outlet.status}), 200

@app.route("/outlets/<int:outlet_id>/status", methods=["POST"])
def update_outlet_status(outlet_id):
    outlet = Outlet.query.get(outlet_id)
    if not outlet:
        return jsonify({"error": "Outlet not found"}), 404
    data = request.get_json()
    new_status = data.get("outlet_status")
    if new_status not in ["on", "off"]:
        return jsonify({"error": "Invalid status"}), 400
    outlet.status = new_status
    db.session.commit()
    return jsonify({"message": "Outlet status updated", "status": outlet.status}), 200

@app.route("/sensors/<string:sensor_type>/data", methods=["POST"])
def add_sensor_data(sensor_type):
    data = request.get_json()
    value = data.get("value")
    if value is None:
        return jsonify({"error": "Missing value"}), 400

    sensor = Sensor.query.filter_by(type=sensor_type).first()
    if not sensor:
        return jsonify({"error": f"Sensor {sensor_type} not found"}), 404

    new_data = SensorData(sensor_id=sensor.id, value=value)
    db.session.add(new_data)
    db.session.commit()
    return jsonify({"message": "Sensor data added"}), 201

@app.route("/sensors/<string:sensor_type>/latest", methods=["GET"])
def get_latest_sensor_data(sensor_type):
    sensor = Sensor.query.filter_by(type=sensor_type).first()
    if not sensor:
        return jsonify({"error": f"Sensor '{sensor_type}' not found"}), 404

    latest = SensorData.query.filter_by(sensor_id=sensor.id).order_by(SensorData.timestamp.desc()).first()
    if not latest:
        return jsonify({"error": f"No data for sensor '{sensor_type}'"}), 404

    return jsonify({
        "sensor_id": sensor.id,
        "type": sensor.type,
        "value": latest.value,
        "timestamp": latest.timestamp.isoformat()
    }), 200

@app.route("/sensors/<string:sensor_type>/history", methods=["GET"])
def get_sensor_history(sensor_type):
    sensor = Sensor.query.filter_by(type=sensor_type).first()
    if not sensor:
        return jsonify({"error": f"Sensor '{sensor_type}' not found"}), 404

    entries = SensorData.query.filter_by(sensor_id=sensor.id).order_by(SensorData.timestamp.asc()).all()
    return jsonify([
        {
            "timestamp": entry.timestamp.strftime("%d.%m"),
            "value": entry.value
        } for entry in entries
    ]), 200

@app.route("/lightbulbs/<int:lightbulb_id>", methods=["GET"])
def get_lightbulb(lightbulb_id):
    lightbulb = Lightbulb.query.get(lightbulb_id)
    if not lightbulb:
        return jsonify({"error": "Lightbulb not found"}), 404

    return jsonify({
        "id": lightbulb.id,
        "status": lightbulb.status,
        "sensor_id": lightbulb.sensor_id
    }), 200

@app.route("/lightbulbs/<int:lightbulb_id>", methods=["PATCH"])
def update_lightbulb(lightbulb_id):
    lightbulb = Lightbulb.query.get(lightbulb_id)
    if not lightbulb:
        return jsonify({"error": "Lightbulb not found"}), 404

    data = request.get_json()
    new_status = data.get("status")
    if new_status not in ["on", "off", "auto"]:
        return jsonify({"error": "Invalid status"}), 400

    lightbulb.status = new_status
    cmd = f"turn_{new_status}_led"
    if new_status == "auto":
        cmd = "set_led_auto"
    try:
        response = requests.post(DOWNLINK_URL, json={"methodName": "execute", "payload": {"command": cmd}})
        if response.status_code != 200:
            return jsonify({"error": "Failed to toggle outlet status"}), 500
    except requests.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500
    db.session.commit()
    return jsonify({"message": "Lightbulb updated", "status": lightbulb.status}), 200

@app.route("/lightbulbs/<int:lightbulb_id>/status", methods=["POST"])
def update_lightbulb_status(lightbulb_id):
    lightbulb = Lightbulb.query.get(lightbulb_id)
    if not lightbulb:
        return jsonify({"error": "Lightbulb not found"}), 404
    data = request.get_json()
    new_status = data.get("lightbulb_status")
    if new_status not in ["on", "off", "auto"]:
        return jsonify({"error": "Invalid status"}), 400
    lightbulb.status = new_status
    db.session.commit()
    return jsonify({"message": "Lightbulb status updated", "status": lightbulb.status}), 200

if __name__ == '__main__':
    with app.app_context():
        for i in range(10):
            try:
                db.drop_all()
                db.create_all()

                def ensure_sensor(sensor_type):
                    existing = Sensor.query.filter_by(type=sensor_type).first()
                    if not existing:
                        sensor = Sensor(type=sensor_type)
                        db.session.add(sensor)
                        db.session.commit()
                        print(f"✅ Sensor '{sensor_type}' created.")

                for sensor_type in ['power', 'voltage', 'amperage', 'total', 'temperature', 'humidity']:
                    ensure_sensor(sensor_type)


                if Outlet.query.get(1) is None:
                    outlet = Outlet(
                        id=1,
                        status='off',
                        power_sensor_id=Sensor.query.filter_by(type='power').first().id,
                        voltage_sensor_id=Sensor.query.filter_by(type='voltage').first().id,
                        amperage_sensor_id=Sensor.query.filter_by(type='amperage').first().id,
                        total_sensor_id=Sensor.query.filter_by(type='total').first().id,
                    )
                    db.session.add(outlet)
                    db.session.commit()
                    print("🔌 Outlet #1 created.")

                if Lightbulb.query.get(1) is None:
                    lightbulb = Lightbulb(
                        id=1,
                        status='off',
                        sensor_id=None
                    )
                    db.session.add(lightbulb)
                    db.session.commit()
                    print("💡 Lightbulb #1 created.")

                print("✅ Tables dropped and created successfully.")
                break
            except OperationalError:
                print(f"DB not ready yet ({i+1}/10). Retrying in 3s...")
                time.sleep(3)
        else:
            print("❌ Could not connect to DB after 10 attempts.")
            exit(1)

    app.run(host='0.0.0.0', port=8000, debug=True)

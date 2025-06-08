from sqlite3 import OperationalError
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS
import time

from extensions import db, jwt
from models import Property, Reservation, Outlet

app = Flask(__name__)

# Konfiguracja
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/smartrent'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

# Inicjalizacja rozszerzeń
CORS(app)
db.init_app(app)
jwt.init_app(app)

# ROUTY

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

    new_property = Property(
        user_id=user_id,
        status=status,
        description=description,
        price=price
    )

    db.session.add(new_property)
    db.session.commit()

    return jsonify({"message": "Property added successfully"}), 201


@app.route("/properties/public", methods=["GET"])
def get_all_properties_public():
    properties = Property.query.filter_by(status="Active").all()
    return jsonify([
        {
            "id": prop.id,
            "status": prop.status,
            "description": prop.description,
            "price": prop.price,
            "name": f"Mieszkanie #{prop.id}"
        } for prop in properties
    ]), 200


@app.route("/properties", methods=["GET"])
@jwt_required()
def get_user_properties():
    user_id = get_jwt_identity()
    properties = Property.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "id": prop.id,
            "status": prop.status,
            "description": prop.description,
            "price": prop.price
        } for prop in properties
    ]), 200


@app.route("/reservations", methods=["GET"])
@jwt_required()
def get_user_reservations():
    user_id = get_jwt_identity()
    reservations = Reservation.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "id": res.id,
            "property_id": res.property_id,
            "start_date": res.start_date.isoformat(),
            "end_date": res.end_date.isoformat(),
            "status": res.status
        } for res in reservations
    ]), 200

@app.route("/outlets/<int:outlet_id>/status", methods=["GET"])
def get_outlet_status(outlet_id):
    outlet = Outlet.query.get(outlet_id)
    if not outlet:
        return jsonify({"error": "Outlet not found"}), 404

    return jsonify({
        "status": outlet.status,
        "power_consumption": outlet.power_consumption,
        "amparage": outlet.amparage,
        "voltage": outlet.voltage
    }), 200



@app.route("/outlets/<int:outlet_id>/toggle", methods=["POST"])
def toggle_outlet_status(outlet_id):
    outlet = Outlet.query.get(outlet_id)
    if not outlet:
        return jsonify({"error": "Outlet not found"}), 404
    outlet.status = "off" if outlet.status == "on" else "on"
    db.session.commit()
    return jsonify({"message": "Outlet status updated", "status": outlet.status}), 200


# if __name__ == '__main__':
#     with app.app_context():
#         for i in range(10):
#             try:
#                 db.drop_all()
#                 db.create_all()
#                 print("Tables dropped and created successfully.")
#                 break
#             except OperationalError as e:
#                 print(f"DB not ready yet ({i+1}/10). Retrying in 3s...")
#                 time.sleep(3)
#         else:
#             print("❌ Could not connect to DB after 10 attempts.")
#             exit(1)
#     app.run(host='0.0.0.0', port=8000, debug=True)
if __name__ == '__main__':
    with app.app_context():
        for i in range(10):
            try:
                db.drop_all()
                db.create_all()

                # 🔌 Dodanie testowego gniazdka o ID 1, jeśli nie istnieje
                if Outlet.query.get(1) is None:
                    db.session.add(Outlet(id=1, status='off'))
                    db.session.commit()
                    print("🔌 Outlet #1 added to DB")

                print("Tables dropped and created successfully.")
                break
            except OperationalError as e:
                print(f"DB not ready yet ({i+1}/10). Retrying in 3s...")
                time.sleep(3)
        else:
            print("❌ Could not connect to DB after 10 attempts.")
            exit(1)

    app.run(host='0.0.0.0', port=8000, debug=True)

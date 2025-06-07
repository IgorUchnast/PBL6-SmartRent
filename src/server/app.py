from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS

from extensions import db, jwt
from models import Property, Reservation

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


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Tables dropped and created successfully.")
    app.run(host='0.0.0.0', port=8000, debug=True)

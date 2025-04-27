from datetime import timedelta
from flask import Blueprint, jsonify, request
from .models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

# --- Blueprint -----------------------------------------------------------------
auth = Blueprint("auth", __name__)          # poprawka – __name__ zamiast "__name__"

# ------------------------------------------------------------------------------
#  REGISTER
# ------------------------------------------------------------------------------
@auth.route("/register", methods=["POST"])
def register() -> tuple[dict, int]:
    """
    POST /register
    Body (JSON): { "name": str, "email": str, "password": str }
    """
    data = request.get_json() or {}
    name: str | None = data.get("name")
    email: str | None = data.get("email")
    password: str | None = data.get("password")

    # Walidacja merytoryczna ----------------------------------------------------
    if not name or not email or not password:
        return jsonify({"message": "Imię, e-mail i hasło są wymagane."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Użytkownik z tym e-mailem już istnieje."}), 400

    # Utworzenie + zapis użytkownika -------------------------------------------
    new_user = User(name=name, email=email)
    new_user.set_password(password)        # zapisze hash w kolumnie LargeBinary

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Rejestracja zakończona sukcesem."}), 201


# ------------------------------------------------------------------------------
#  LOGIN
# ------------------------------------------------------------------------------
@auth.route("/login", methods=["POST"])
def login() -> tuple[dict, int]:
    """
    POST /login
    Body (JSON): { "email": str, "password": str }
    """
    data = request.get_json() or {}
    email: str | None = data.get("email")
    password: str | None = data.get("password")

    if not email or not password:
        return jsonify({"message": "E-mail i hasło są wymagane."}), 400

    user: User | None = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Nieprawidłowy e-mail lub hasło."}), 401

    access_token: str = user.generate_jwt()   # 60-minutowy token wg modelu User
    return (
        jsonify({"message": "Logowanie udane.", "access_token": access_token}),
        200,
    )

# app.py
from datetime import datetime, timedelta
from enum import Enum as PyEnum

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.types import Numeric
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret-change-me"

db = SQLAlchemy(app)
jwt = JWTManager(app)

# ---------- Mixin z automatycznymi znacznikami czasu -------------------------
class TimestampMixin(object):
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

# ---------- Enums -> String + CheckConstraint --------------------------------
class PropertyStatus(PyEnum):
    FREE = "free"
    RESERVED = "reserved"
    UNAVAILABLE = "unavailable"

class ReservationStatus(PyEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

# ---------- MODELE -----------------------------------------------------------
class User(TimestampMixin, db.Model):
    __tablename__ = "users"
    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.LargeBinary(60), nullable=False)
    name          = db.Column(db.String(100), nullable=False)

    # relacje
    properties    = db.relationship("Property", back_populates="owner",
                                    cascade="all, delete-orphan")
    reservations  = db.relationship("Reservation", back_populates="guest",
                                    cascade="all, delete-orphan")

    # --- metody pomocnicze
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def generate_jwt(self) -> str:
        return create_access_token(
            identity=self.id,
            expires_delta=timedelta(hours=1),
            additional_claims={"email": self.email},
        )

class Property(TimestampMixin, db.Model):
    __tablename__ = "properties"
    id          = db.Column(db.Integer, primary_key=True)
    owner_id    = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                            nullable=False)
    status      = db.Column(db.String(12), nullable=False,
                            default=PropertyStatus.FREE.value)
    description = db.Column(db.String(500))
    price       = db.Column(Numeric(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint(
            f"status IN ('{PropertyStatus.FREE.value}', "
            f"'{PropertyStatus.RESERVED.value}', "
            f"'{PropertyStatus.UNAVAILABLE.value}')",
            name="ck_property_status",
        ),
    )

    owner        = db.relationship("User", back_populates="properties")
    reservations = db.relationship("Reservation", back_populates="property_",
                                   cascade="all, delete-orphan")

class Reservation(TimestampMixin, db.Model):
    __tablename__ = "reservations"
    id          = db.Column(db.Integer, primary_key=True)
    guest_id    = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                            nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id", ondelete="CASCADE"),
                            nullable=False)
    start_date  = db.Column(db.DateTime(timezone=True), nullable=False)
    end_date    = db.Column(db.DateTime(timezone=True),   nullable=False)
    status      = db.Column(db.String(10), nullable=False,
                            default=ReservationStatus.PENDING.value)

    __table_args__ = (
        CheckConstraint("end_date > start_date", name="ck_res_period"),
        UniqueConstraint("property_id", "start_date", "end_date",
                         name="uq_property_dates"),
        CheckConstraint(
            f"status IN ('{ReservationStatus.PENDING.value}', "
            f"'{ReservationStatus.CONFIRMED.value}', "
            f"'{ReservationStatus.CANCELLED.value}')",
            name="ck_res_status",
        ),
    )

    guest     = db.relationship("User", back_populates="reservations")
    property_ = db.relationship("Property", back_populates="reservations")

# ---------- ENDPOINT testowy -------------------------------------------------
@app.route("/ping")
def ping():
    return jsonify({"msg": "pong", "time": datetime.utcnow().isoformat()})

# ---------- MAIN -------------------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()          # utworzenie struktury w app.db
    app.run(debug=True)

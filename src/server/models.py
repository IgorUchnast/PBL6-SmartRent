"""ORM models for the short-term-rental platform (SQLite edition).

• One central SQLAlchemy instance (`db`) – import this file *after* you initialise
  `db = SQLAlchemy(app)` in your Flask application.
• Designed for SQLite 3.x: ENUMs are implemented as strings with `CheckConstraint`.
• All timestamps are stored in UTC ISO format; handled transparently by SQLAlchemy.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum as PyEnum

from flask_jwt_extended import create_access_token
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import LargeBinary, Numeric
from werkzeug.security import generate_password_hash, check_password_hash

# Assuming `db` is created in your Flask app and imported here
from .app import db  # adjust the import path as needed

###############################################################################
# Mixins
###############################################################################

class TimestampMixin:  # pylint: disable=too-few-public-methods
    """Automatically add *created_at* and *updated_at* columns to a model."""

    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

###############################################################################
# Helper Enums  (represented as TEXT in SQLite + CheckConstraint)
###############################################################################

class PropertyStatus(PyEnum):
    FREE = "free"
    RESERVED = "reserved"
    UNAVAILABLE = "unavailable"

class ReservationStatus(PyEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class BillingStatus(PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class DeviceType(PyEnum):
    SENSOR = "sensor"
    OUTLET = "outlet"
    LIGHTBULB = "lightbulb"

###############################################################################
# Core domain models
###############################################################################

class User(TimestampMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    password_hash: Mapped[bytes] = mapped_column(LargeBinary(60), nullable=False)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)

    # relationships
    properties: Mapped[list["Property"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )
    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="guest", cascade="all, delete-orphan"
    )
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )

    # ---------------------------------------------------------------------
    # Helper methods
    # ---------------------------------------------------------------------
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def generate_jwt(self, expires: timedelta | None = None) -> str:
        """Return a short-lived access-token.

        Default expiry: 1 hour.
        """
        expires = expires or timedelta(hours=1)
        return create_access_token(
            identity=self.id,
            expires_delta=expires,
            additional_claims={"email": self.email},
        )

###############################################################################

class Property(TimestampMixin, db.Model):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        db.String(12), nullable=False, default=PropertyStatus.FREE.value
    )
    description: Mapped[str | None] = mapped_column(db.String(500))
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "status IN ('free','reserved','unavailable')", name="ck_property_status"
        ),
    )

    # relationships
    owner: Mapped[User] = relationship(back_populates="properties")
    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="property_", cascade="all, delete-orphan"
    )
    devices: Mapped[list["Device"]] = relationship(
        back_populates="property_", cascade="all, delete-orphan"
    )

###############################################################################

class Reservation(TimestampMixin, db.Model):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True)
    guest_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    property_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("properties.id", ondelete="CASCADE"), nullable=False
    )
    start_date: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(
        db.String(10), nullable=False, default=ReservationStatus.PENDING.value
    )

    __table_args__ = (
        CheckConstraint("end_date > start_date", name="ck_res_period"),
        UniqueConstraint("property_id", "start_date", "end_date", name="uq_property_dates"),
        CheckConstraint(
            "status IN ('pending','confirmed','cancelled')", name="ck_res_status"
        ),
    )

    # relationships
    guest: Mapped[User] = relationship(back_populates="reservations")
    property_: Mapped[Property] = relationship(back_populates="reservations")
    billing: Mapped["Billing" | None] = relationship(
        back_populates="reservation", uselist=False, cascade="all, delete-orphan"
    )

###############################################################################

class Billing(TimestampMixin, db.Model):
    __tablename__ = "billings"

    id: Mapped[int] = mapped_column(primary_key=True)
    reservation_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey("reservations.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(
        db.String(10), nullable=False, default=BillingStatus.PENDING.value
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending','completed','failed')", name="ck_billing_status"
        ),
    )

    reservation: Mapped[Reservation] = relationship(back_populates="billing")

###############################################################################

class Review(TimestampMixin, db.Model):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    property_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("properties.id", ondelete="CASCADE"), nullable=False
    )
    rating: Mapped[int] = mapped_column(db.Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(db.String(500))

    __table_args__ = (
        CheckConstraint("rating BETWEEN 1 AND 5", name="ck_review_rating"),
    )

    # relationships
    author: Mapped[User] = relationship(back_populates="reviews")
    property: Mapped[Property] = relationship()

###############################################################################
# Polymorphic device hierarchy
###############################################################################

class Device(TimestampMixin, db.Model):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    property_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("properties.id", ondelete="CASCADE"), nullable=False
    )
    device_type: Mapped[str] = mapped_column(db.String(12), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": device_type,
        "polymorphic_identity": "device",
    }

    property_: Mapped[Property] = relationship(back_populates="devices")

###############################################################################

class Sensor(Device):
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("devices.id", ondelete="CASCADE"), primary_key=True
    )
    sensor_kind: Mapped[str | None] = mapped_column(db.String(50))
    last_value: Mapped[float | None] = mapped_column(db.Float)

    __mapper_args__ = {"polymorphic_identity": DeviceType.SENSOR.value}

    data: Mapped[list["SensorData"]] = relationship(
        back_populates="sensor", cascade="all, delete-orphan"
    )

###############################################################################

class SensorData(db.Model):
    __tablename__ = "sensor_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("sensors.id", ondelete="CASCADE"), nullable=False
    )
    timestamp: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    value: Mapped[float] = mapped_column(db.Float)

    sensor: Mapped[Sensor] = relationship(back_populates="data")

###############################################################################

class Outlet(Device):
    __tablename__ = "outlets"

    id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("devices.id", ondelete="CASCADE"), primary_key=True
    )
    status: Mapped[str] = mapped_column(db.String(3), default="off")  # on/off
    power_watt: Mapped[float] = mapped_column(db.Float, default=0.0)

    __mapper_args__ = {"polymorphic_identity": DeviceType.OUTLET.value}

###############################################################################

class Lightbulb(Device):
    __tablename__ = "lightbulbs"

    id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("devices.id", ondelete="CASCADE"), primary_key=True
    )
    status: Mapped[str] = mapped_column(db.String(3), default="off")
    sensor_id: Mapped[int | None] = mapped_column(
        db.Integer, db.ForeignKey("sensors.id", ondelete="SET NULL"), nullable=True
    )

    __mapper_args__ = {"polymorphic_identity": DeviceType.LIGHTBULB.value}

    sensor: Mapped[Sensor | None] = relationship()

###############################################################################
# Utility function for first-time DB creation
###############################################################################


def create_all_tables() -> None:  # pragma: no cover
    """Convenience wrapper – call once at app start-up inside *app_context*."""

    db.create_all()
    print("[DB] All tables created (SQLite)")

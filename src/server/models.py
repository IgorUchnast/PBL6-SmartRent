from extensions import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_jwt(self):
        return create_access_token(identity=str(self.id), expires_delta=timedelta(days=10))


class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(20), nullable=True, default='free')  # 'free', 'reserved', 'unavailable'
    description = db.Column(db.String(500), nullable=True)
    adress = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=True)


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id', ondelete='CASCADE'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=True, default='pending')  # 'pending', 'confirmed', 'cancelled'


class Billing(db.Model):
    __tablename__ = 'billings'
    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=True, default='pending')  # 'pending', 'completed', 'failed'


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500), nullable=True)


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=True)


class Outlet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), default='off')

    power_sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))
    voltage_sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))
    amperage_sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))
    total_sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))

    power_sensor = db.relationship('Sensor', foreign_keys=[power_sensor_id])
    voltage_sensor = db.relationship('Sensor', foreign_keys=[voltage_sensor_id])
    amperage_sensor = db.relationship('Sensor', foreign_keys=[amperage_sensor_id])
    total_sensor = db.relationship('Sensor', foreign_keys=[total_sensor_id])


class Sensor(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # e.g., power, voltage, amperage, total

    # ❌ USUŃ TĘ LINIĘ (bo powoduje błąd):
    # outlet = db.relationship('Outlet', backref='sensor', uselist=False)

    lightbulbs = db.relationship('Lightbulb', backref='sensor')
    data = db.relationship('SensorData', backref='sensor', cascade='all, delete-orphan')


class SensorData(db.Model):
    __tablename__ = 'sensor_data'
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id', ondelete='CASCADE'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    value = db.Column(db.Float, nullable=False)


class Lightbulb(db.Model):
    __tablename__ = 'lightbulbs'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), default='off')  # on, off, auto
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id', ondelete='SET NULL'), nullable=True)

    # ❗ Nie trzeba definiować tu relationship – jest już w `Sensor.lightbulbs` dzięki backref

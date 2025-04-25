from app import db
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String)
    name = db.Column(db.String(100))

    def set_password(self, password):
        # Hash the password when setting it
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Check if the provided password matches the stored hash
        return check_password_hash(self.password_hash, password)

    def generate_jwt(self):
        # Generate JWT token for the user that expires after 10 days
        return create_access_token(identity=str(self.id), expires_delta=timedelta(days=10))


class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))  # Whose property it is
    status = db.Column(db.String(20), nullable=True, default='free')  # 'free', 'reserved', 'unavailable'
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float)


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))  # Who made the reservation
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id', ondelete='CASCADE'))  # Which property is reserved
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), nullable=True, default='pending')  # 'pending', 'confirmed', 'cancelled'
    # 'pending' - waiting for confirmation from the owner
    # 'confirmed' - owner confirmed the reservation
    # 'cancelled' - reservation was cancelled by either party


class Billing(db.Model):
    __tablename__ = 'billings'
    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id', ondelete='CASCADE'))  # Which reservation is paid for
    amount = db.Column(db.Float)
    status = db.Column(db.String(20), nullable=True, default='pending')  # 'pending', 'completed', 'failed'
    # 'pending' - payment is being processed
    # 'completed' - payment was successful
    # 'failed' - payment failed


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))  # Who wrote the review
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id', ondelete='CASCADE'))  # Which property is being reviewed
    rating = db.Column(db.Integer)  # Rating from 1 to 5
    comment = db.Column(db.String(500), nullable=True)  # Review comment


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id', ondelete='CASCADE'))  # Which property the device belongs to


class Sensor(Device):
    __tablename__ = 'sensors'
    type = db.Column(db.String(50))  # Type of sensor (e.g., temperature, humidity, etc.)
    value = db.Column(db.Float)  # Current value of the sensor


class SensorData(db.Model):
    __tablename__ = 'sensor_data'
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id', ondelete='CASCADE'))  # Which sensor the data belongs to
    timestamp = db.Column(db.DateTime)  # When the data was recorded
    value = db.Column(db.Float)  # Value of the sensor at the given timestamp
    # Additional fields can be added as needed for specific sensor types


class Outlet(Device):
    __tablename__ = 'outlets'
    status = db.Column(db.String(20), default='off')  # 'on' or 'off'
    power_consumption = db.Column(db.Float, default=0.0)  # Power consumption in watts


class Lightbulb(Device):
    __tablename__ = 'lightbulbs'
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id', ondelete='CASCADE'))  # Which sensor the lightbulb is associated with
    # brightness = db.Column(db.Integer, default=0)  # Brightness level (0-100)
    status = db.Column(db.String(20), default='off')  # 'on' or 'off'

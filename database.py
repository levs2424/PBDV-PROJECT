import datetime
from flask_sqlalchemy import SQLAlchemy
from enum import Enum as PyEnum

db = SQLAlchemy()

# User Roles Enum
class UserRole(PyEnum):
    STUDENT = "Student"
    TUTOR = "Tutor"
    ADMIN = "Admin"

# Booking Status Enum
class BookingStatus(PyEnum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"

# Qualification Status Enum
class QualificationStatus(PyEnum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

# Users Table
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tutor_profile = db.relationship("Tutor", back_populates="user", uselist=False)

# Tutors Table
class Tutor(db.Model):
    __tablename__ = "tutors"

    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    bio = db.Column(db.Text)
    hourly_rate = db.Column(db.Numeric(10, 2))
    is_verified = db.Column(db.Boolean, default=False)

    user = db.relationship("User", back_populates="tutor_profile")
    qualifications = db.relationship("Qualification", back_populates="tutor")
    availability = db.relationship("Availability", back_populates="tutor")
    bookings = db.relationship("Booking", back_populates="tutor")

# Qualifications Table
class Qualification(db.Model):
    __tablename__ = "qualifications"

    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey("tutors.id"), nullable=False)
    document_path = db.Column(db.String(255))
    test_score = db.Column(db.Numeric(5, 2))
    status = db.Column(db.Enum(QualificationStatus), default=QualificationStatus.PENDING)

    tutor = db.relationship("Tutor", back_populates="qualifications")

# Availability Table
class Availability(db.Model):
    __tablename__ = "availability"

    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey("tutors.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    tutor = db.relationship("Tutor", back_populates="availability")

# Bookings Table
class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey("tutors.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(BookingStatus), default=BookingStatus.PENDING)

    student = db.relationship("User", foreign_keys=[student_id])
    tutor = db.relationship("Tutor", back_populates="bookings")

# Reviews Table
class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Messages Table
class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

# Notifications Table
class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

print("Loading model.py")
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student' or 'tutor'

    
    tutor_modules = relationship("TutorModule", back_populates="tutor", lazy=True)
    availability = relationship("TutorAvailability", back_populates="tutor", lazy=True)
    bookings_as_student = relationship("Booking", foreign_keys="Booking.student_id", back_populates="student", lazy=True)
    bookings_as_tutor = relationship("Booking", foreign_keys="Booking.tutor_id", back_populates="tutor", lazy=True)


class Module(db.Model):
    __tablename__ = 'modules'
    module_id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    module_code = db.Column(db.String(20), nullable=False)

    
    tutor_modules = relationship("TutorModule", back_populates="module", lazy=True)
    availabilities = relationship("TutorAvailability", back_populates="module", lazy=True)
    bookings = relationship("Booking", back_populates="module", lazy=True)


class TutorModule(db.Model):
    __tablename__ = 'tutor_modules'
    tutor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.module_id'), primary_key=True)

    
    tutor = relationship("User", back_populates="tutor_modules")
    module = relationship("Module", back_populates="tutor_modules")


class TutorAvailability(db.Model):
    __tablename__ = 'tutor_availability'
    availability_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.module_id'), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    
    tutor = relationship("User", back_populates="availability")
    module = relationship("Module", back_populates="availabilities")
    bookings = relationship("Booking", back_populates="availability", lazy=True)

    __table_args__ = (db.UniqueConstraint('tutor_id', 'module_id', 'day_of_week', 'start_time', 'end_time'),)


class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.module_id'), nullable=False)
    availability_id = db.Column(db.Integer, db.ForeignKey('tutor_availability.availability_id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)

    
    student = relationship("User", foreign_keys="Booking.student_id", back_populates="bookings_as_student")
    tutor = relationship("User", foreign_keys="Booking.tutor_id", back_populates="bookings_as_tutor")
    module = relationship("Module", back_populates="bookings")
    availability = relationship("TutorAvailability", back_populates="bookings")

    __table_args__ = (db.UniqueConstraint('tutor_id', 'module_id', 'booking_date', 'availability_id'),)
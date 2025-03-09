from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, Time, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import re

Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = 'users'

    student_num = Column(String(8), primary_key=True)
    student_name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    tutor_profile = relationship("TutorProfile", uselist=False, back_populates="user")
    bookings_as_student = relationship("LessonBooking", foreign_keys="LessonBooking.student_num", back_populates="student")
    bookings_as_tutor = relationship("LessonBooking", foreign_keys="LessonBooking.tutor_id", back_populates="tutor")

    def __init__(self, student_num, student_name, email, password, role):
        if not re.match(r'^\d{8}$', student_num):
            raise ValueError("StudentNum must be exactly 8 digits")
        self.student_num = student_num
        self.student_name = student_name
        self.email = email
        self.password = password
        self.role = role

    def check_role(self, role_to_check):
        return role_to_check in self.role.split(',')

# Tutor Profile Model
class TutorProfile(Base):
    __tablename__ = 'tutor_profiles'

    tutor_id = Column(Integer, primary_key=True, autoincrement=True)
    student_num = Column(String(8), ForeignKey('users.student_num'), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    subjects = Column(String, nullable=False)
    hourly_rate = Column(Integer, nullable=False)
    day_of_week = Column(Enum('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', name='day_of_week'), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_recurring = Column(Boolean, default=False)

    user = relationship("User", back_populates="tutor_profile")

# Lesson Booking Model
class LessonBooking(Base):
    __tablename__ = 'lesson_bookings'

    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    student_num = Column(String(8), ForeignKey('users.student_num'), nullable=False)
    tutor_id = Column(String(8), ForeignKey('users.student_num'), nullable=False)
    subject = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(Enum('pending', 'confirmed', 'completed', 'canceled', name='status'), default='pending')

    student = relationship("User", foreign_keys=[student_num], back_populates="bookings_as_student")
    tutor = relationship("User", foreign_keys=[tutor_id], back_populates="bookings_as_tutor")
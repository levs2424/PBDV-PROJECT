import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# User Model
class User(db.Model):
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('Student', 'Tutor', 'Admin', name="user_roles"), nullable=False, default='Student')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name} - {self.role}>'


# Tutor Model
class Tutor(db.Model):
    __tablename__ = 'Tutors'

    tutor_id = db.Column(db.Integer, db.ForeignKey('Users.user_id', ondelete="CASCADE"), primary_key=True)
    bio = db.Column(db.Text, nullable=True)
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('tutor_profile', uselist=False, cascade="all, delete"))

    def __repr__(self):
        return f'<Tutor {self.tutor_id} - Verified: {self.is_verified}>'


# Qualifications Model
class Qualification(db.Model):
    __tablename__ = 'Qualifications'

    qualification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('Tutors.tutor_id', ondelete="CASCADE"), nullable=False)
    document_path = db.Column(db.String(255), nullable=True)
    test_score = db.Column(db.Numeric(5, 2), nullable=True)
    status = db.Column(db.Enum('Pending', 'Approved', 'Rejected', name="qualification_status"), default='Pending')

    tutor = db.relationship('Tutor', backref='qualifications')

    def __repr__(self):
        return f'<Qualification {self.qualification_id} - {self.status}>'


# Availability Model
class Availability(db.Model):
    __tablename__ = 'Availability'

    availability_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('Tutors.tutor_id', ondelete="CASCADE"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    tutor = db.relationship('Tutor', backref='availability')

    def __repr__(self):
        return f'<Availability {self.availability_id} - {self.start_time} to {self.end_time}>'


# Booking Model
class Booking(db.Model):
    __tablename__ = 'Bookings'

    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('Users.user_id', ondelete="CASCADE"), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('Tutors.tutor_id', ondelete="CASCADE"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('Pending', 'Confirmed', 'Cancelled', name="booking_status"), default='Pending')

    student = db.relationship('User', foreign_keys=[student_id], backref='bookings_made')
    tutor = db.relationship('Tutor', foreign_keys=[tutor_id], backref='bookings_received')

    def __repr__(self):
        return f'<Booking {self.booking_id} - {self.status}>'


# Reviews Model
class Review(db.Model):
    __tablename__ = 'Reviews'

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('Bookings.booking_id', ondelete="CASCADE"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    booking = db.relationship('Booking', backref='reviews')

    def __repr__(self):
        return f'<Review {self.review_id} - {self.rating} stars>'


# Messages Model
class Message(db.Model):
    __tablename__ = 'Messages'

    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('Users.user_id', ondelete="CASCADE"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('Users.user_id', ondelete="CASCADE"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='messages_sent')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='messages_received')

    def __repr__(self):
        return f'<Message {self.message_id} - Sent by {self.sender_id} to {self.receiver_id}>'


# Notifications Model
class Notification(db.Model):
    __tablename__ = 'Notifications'

    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id', ondelete="CASCADE"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user = db.relationship('User', backref='notifications')

    def __repr__(self):
        return f'<Notification {self.notification_id} - Read: {self.is_read}>'

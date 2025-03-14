from flask_wtf import FlaskForm
from wtforms import (
    PasswordField, SelectField, StringField, TextAreaField, SubmitField, DecimalField, 
    BooleanField, DateTimeField, IntegerField
)
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange, Optional

# User SignUp Form
class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, max=255),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('Student', 'Student'), ('Tutor', 'Tutor'), ('Admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
    
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('Student', 'Student'), ('Tutor', 'Tutor'), ('Admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

# Tutor Profile Form
class TutorProfileForm(FlaskForm):
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)])
    hourly_rate = DecimalField('Hourly Rate', validators=[Optional(), NumberRange(min=0)], places=2)
    is_verified = BooleanField('Verified')
    submit = SubmitField('Update Profile')

# Qualification Form
class QualificationForm(FlaskForm):
    document_path = StringField('Document Path', validators=[Optional(), Length(max=255)])
    test_score = DecimalField('Test Score', validators=[Optional(), NumberRange(min=0, max=100)], places=2)
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], validators=[DataRequired()])
    submit = SubmitField('Submit Qualification')

# Availability Form
class AvailabilityForm(FlaskForm):
    start_time = DateTimeField('Start Time', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    end_time = DateTimeField('End Time', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    submit = SubmitField('Set Availability')

# Booking Form
class BookingForm(FlaskForm):
    tutor_id = IntegerField('Tutor ID', validators=[DataRequired()])
    start_time = DateTimeField('Start Time', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    end_time = DateTimeField('End Time', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], validators=[DataRequired()])
    submit = SubmitField('Book Session')

# Review Form
class ReviewForm(FlaskForm):
    booking_id = IntegerField('Booking ID', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Comment', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Submit Review')

# Message Form
class MessageForm(FlaskForm):
    receiver_id = IntegerField('Receiver ID', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Send Message')

# Notification Form
class NotificationForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[DataRequired()])
    message = TextAreaField('Notification Message', validators=[DataRequired(), Length(max=500)])
    is_read = BooleanField('Mark as Read')
    submit = SubmitField('Send Notification')

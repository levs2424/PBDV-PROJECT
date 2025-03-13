# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Module, TutorModule, TutorAvailability, Booking
from datetime import datetime, date
import os


app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'peer_tutoring.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # For session management and flash messages


db.init_app(app)


with app.app_context():
    db.create_all()


@app.route('/logout')
def logout():
    
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/view_bookings')
def view_bookings():
    if 'user_id' not in session or session['role'] != 'student':
        flash('Please log in as a student', 'error')
        return redirect(url_for('login'))

    
    student_id = session['user_id']
    bookings = Booking.query.filter_by(student_id=student_id).all()
    return render_template('view_bookings.html', bookings=bookings)


@app.route('/users')
def list_users():
    users = User.query.all()
    return str([(u.username, u.password, u.role) for u in users])


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.user_id
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'error')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session['role'] == 'student':
        return redirect(url_for('student_dashboard'))
    return "Tutor Dashboard"  


@app.route('/student_dashboard')
def student_dashboard():
    if 'user_id' not in session or session['role'] != 'student':
        flash('Please log in as a student', 'error')
        return redirect(url_for('login'))
    modules = Module.query.all()
    return render_template('student_dash.html', modules=modules)


@app.route('/book_session/<int:module_id>', methods=['GET', 'POST'])
def book_session(module_id):
    if 'user_id' not in session or session['role'] != 'student':
        flash('Please log in as a student', 'error')
        return redirect(url_for('login'))

    
    module = Module.query.get_or_404(module_id)

    
    tutor_modules = TutorModule.query.filter_by(module_id=module_id).all()
    tutor_ids = [tm.tutor_id for tm in tutor_modules]
    tutors = User.query.filter(User.user_id.in_(tutor_ids), User.role == 'tutor').all()

    if request.method == 'POST':
        tutor_id = int(request.form['tutor_id'])
        availability_id = int(request.form['availability_id'])
        booking_date_str = request.form['booking_date']

       
        try:
            booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Use YYYY-MM-DD.', 'error')
            return redirect(url_for('book_session', module_id=module_id))

        
        availability = TutorAvailability.query.filter_by(
            availability_id=availability_id,
            tutor_id=tutor_id,
            module_id=module_id
        ).first()

        if not availability:
            flash('Invalid availability slot.', 'error')
            return redirect(url_for('book_session', module_id=module_id))

        
        days_of_week = {
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5,
            'Sunday': 6
        }

       
        booking_weekday = booking_date.weekday()

       
        if booking_weekday != days_of_week.get(availability.day_of_week):
            flash(f'Invalid date. Please select a date that falls on {availability.day_of_week}.', 'error')
            return redirect(url_for('book_session', module_id=module_id))

        
        if booking_date < date.today():
            flash('Cannot book a session in the past.', 'error')
            return redirect(url_for('book_session', module_id=module_id))

        
        existing_booking = Booking.query.filter_by(
            tutor_id=tutor_id,
            module_id=module_id,
            availability_id=availability_id,
            booking_date=booking_date
        ).first()

        if existing_booking:
            flash('This slot is already booked.', 'error')
            return redirect(url_for('book_session', module_id=module_id))

        
        new_booking = Booking(
            student_id=session['user_id'],
            tutor_id=tutor_id,
            module_id=module_id,
            availability_id=availability_id,
            booking_date=booking_date
        )
        db.session.add(new_booking)
        db.session.commit()

        flash('Booking successful!', 'success')
        return redirect(url_for('student_dashboard'))

    
    selected_tutor_id = request.args.get('tutor_id', type=int)
    availability_slots = []
    if selected_tutor_id:
        availability_slots = TutorAvailability.query.filter_by(
            tutor_id=selected_tutor_id,
            module_id=module_id
        ).all()

    return render_template('book_session.html', module=module, tutors=tutors, availability_slots=availability_slots, selected_tutor_id=selected_tutor_id)


if __name__ == '__main__':
    app.run(debug=True)
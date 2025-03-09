from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import Base, User, TutorProfile, LessonBooking
from datetime import datetime, time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PeerTutoring.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Bind the SQLAlchemy engine to the Base
with app.app_context():
    db.Model.metadata.create_all(db.engine)

# 

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db.session.query(User).filter_by(email=email, password=password).first()
        if user:
            return redirect(url_for('dashboard', student_num=user.student_num))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard/<student_num>')
def dashboard(student_num):
    user = db.session.query(User).filter_by(student_num=student_num).first()
    if not user:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
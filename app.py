from flask import Flask, flash, redirect, render_template, url_for, session
from models import User, db
from forms import LoginForm, SignUpForm
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
import logging

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Set up logging
logging.basicConfig(level=logging.ERROR)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Email address already in use. Please use a different email.', 'danger')
            else:
                hashed_password = generate_password_hash(form.password.data)
                new_user = User(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password_hash=hashed_password,
                    role=form.role.data
                )
                db.session.add(new_user)
                db.session.commit()
                flash('Account created! You can now log in.', 'success')
                print("Redirecting to login page...")  # Debug print
                return redirect(url_for('login'))  # Ensure this is executed
        except Exception as e:
            print(f"Error during signup: {e}")
            logging.error(f"Error during signup: {e}")
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.', 'danger')

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password_hash, form.password.data):
            session['user_id'] = user.user_id  # Store user ID in the session
            flash('Login successful!', 'success')

            print("Redirecting to home page...")  # Debug print
            return redirect(url_for('home'))  # Ensure this is executed
        else:
            flash('Invalid email or password. Please try again.', 'danger')
            print("Invalid email or password...") 
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None) 
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
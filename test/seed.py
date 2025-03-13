from app import app, db
from models import User, Module, TutorModule, TutorAvailability, Booking
from datetime import time, date

def seed_data():
    with app.app_context():
       
        if not User.query.first():
            users = [
                User(username='student1', password='password1', role='student'),
                User(username='tutor1', password='password1', role='tutor'),
                User(username='tutor2', password='password2', role='tutor'),
                User(username='admin', password='admin', role='admin'),
            ]
            db.session.add_all(users)
            db.session.commit()
            print("Users seeded successfully!")
        else:
            print("Users already exist. Skipping user seeding.")

        
        if not Module.query.first():
            modules = [
                Module(module_name='Mathematics', module_code='MATH101', description='Basic Mathematics'),
                Module(module_name='Physics', module_code='PHYS101', description='Introduction to Physics'),
                Module(module_name='Statistics', module_code='STAT101', description='Introduction to Statistics'),
                Module(module_name='Software Engineering', module_code='SWE101', description='Principles of Software Engineering'),
                Module(module_name='Programming Languages', module_code='PROG101', description='Study of Programming Languages'),
                Module(module_name='Networks and Operating Systems', module_code='NOS101', description='Fundamentals of Networks and Operating Systems'),
                Module(module_name='Information Security', module_code='ISEC101', description='Introduction to Information Security'),
                Module(module_name='Platforms-Based Development', module_code='PBD101', description='Development for Specific Platforms'),
                Module(module_name='Integrated Programming', module_code='IPROG101', description='Integrated Programming Techniques'),
                Module(module_name='Research Skills', module_code='RS101', description='Developing Academic Research Skills'),
            ]
            db.session.add_all(modules)
            db.session.commit()
            print("Modules seeded successfully!")
        else:
            print("Modules already exist. Skipping module seeding.")

        
        if not TutorModule.query.first():
            tutor_modules = [
                TutorModule(tutor_id=2, module_id=3),  # tutor1 teaches Statistics
                TutorModule(tutor_id=2, module_id=4),  # tutor1 teaches Software Engineering
                TutorModule(tutor_id=3, module_id=5),  # tutor2 teaches Programming Languages
                TutorModule(tutor_id=3, module_id=6),  # tutor2 teaches Networks and Operating Systems
            ]
            db.session.add_all(tutor_modules)
            db.session.commit()
            print("TutorModules seeded successfully!")
        else:
            print("TutorModules already exist. Skipping TutorModule seeding.")

       
        if not TutorAvailability.query.first():
            tutor_availability = [
                TutorAvailability(tutor_id=2, module_id=3, start_time=time(9, 0), end_time=time(11, 0), day_of_week='Monday'),
                TutorAvailability(tutor_id=2, module_id=4, start_time=time(13, 0), end_time=time(15, 0), day_of_week='Wednesday'),
                TutorAvailability(tutor_id=3, module_id=5, start_time=time(10, 0), end_time=time(12, 0), day_of_week='Tuesday'),
                TutorAvailability(tutor_id=3, module_id=6, start_time=time(14, 0), end_time=time(16, 0), day_of_week='Thursday'),
            ]
            db.session.add_all(tutor_availability)
            db.session.commit()
            print("TutorAvailability seeded successfully!")
        else:
            print("TutorAvailability already exists. Skipping TutorAvailability seeding.")

        
        if not Booking.query.first():
            bookings = [
                Booking(student_id=1, tutor_id=2, module_id=3, availability_id=1, booking_date=date(2023, 10, 30)),
                Booking(student_id=1, tutor_id=3, module_id=5, availability_id=3, booking_date=date(2023, 11, 1)),
            ]
            db.session.add_all(bookings)
            db.session.commit()
            print("Bookings seeded successfully!")
        else:
            print("Bookings already exist. Skipping booking seeding.")

        print("Database seeding completed!")

if __name__ == '__main__':
    seed_data()
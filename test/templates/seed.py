from app import app, db
from models import User, Module, TutorModule, TutorAvailability, Booking
from datetime import time, date

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create Users
        user1 = User(username='student1', password='password1', role='student')
        user2 = User(username='tutor1', password='password2', role='tutor')
        user3 = User(username='tutor2', password='password3', role='tutor')

        db.session.add_all([user1, user2, user3])
        db.session.commit()

        # Create Modules
        module1 = Module(module_name='Mathematics', module_code='MATH101', description='Basic Mathematics')
        module2 = Module(module_name='Physics', module_code='PHYS101', description='Introduction to Physics')

        db.session.add_all([module1, module2])
        db.session.commit()

        # Create TutorModules
        tutor_module1 = TutorModule(tutor_id=user2.user_id, module_id=module1.module_id)
        tutor_module2 = TutorModule(tutor_id=user3.user_id, module_id=module2.module_id)

        db.session.add_all([tutor_module1, tutor_module2])
        db.session.commit()

        # Create TutorAvailability
        availability1 = TutorAvailability(
            tutor_id=user2.user_id,
            module_id=module1.module_id,
            day_of_week='MONDAY',
            start_time=time(10, 0),
            end_time=time(12, 0)
        )
        availability2 = TutorAvailability(
            tutor_id=user3.user_id,
            module_id=module2.module_id,
            day_of_week='TUESDAY',
            start_time=time(14, 0),
            end_time=time(16, 0)
        )

        db.session.add_all([availability1, availability2])
        db.session.commit()

        # Create Bookings
        booking1 = Booking(
            student_id=user1.user_id,
            tutor_id=user2.user_id,
            module_id=module1.module_id,
            availability_id=availability1.availability_id,
            booking_date=date(2023, 10, 10)
        )
        booking2 = Booking(
            student_id=user1.user_id,
            tutor_id=user3.user_id,
            module_id=module2.module_id,
            availability_id=availability2.availability_id,
            booking_date=date(2023, 10, 11)
        )

        db.session.add_all([booking1, booking2])
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()
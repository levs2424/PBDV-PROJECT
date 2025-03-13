from app import app, db
from models import Module

def remove_modules():
    with app.app_context():
        
        math_module = Module.query.filter_by(module_code='MATH101').first()
        physics_module = Module.query.filter_by(module_code='PHYS101').first()

        if math_module:
            db.session.delete(math_module)
            print("Deleted Mathematics module.")
        if physics_module:
            db.session.delete(physics_module)
            print("Deleted Physics module.")

        db.session.commit()
        print("Modules removed successfully!")

if __name__ == '__main__':
    remove_modules()
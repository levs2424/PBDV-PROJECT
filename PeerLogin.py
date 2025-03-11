import bcrypt # type: ignore
from sqlalchemy import create_engine, Column, Integer, String # type: ignore
from sqlalchemy.orm import declarative_base, sessionmaker # type: ignore
import os

# Define the database URL
DATABASE_URL = 'sqlite:////Users/cebomakhuba/Documents/peer_test.db'

# Ensure the directory exists
os.makedirs('/Users/cebomakhuba/Documents', exist_ok=True)

# Create a new SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a base class for declarative models
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'
    
    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Function to create a new user with hashed password
def create_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    role = input("Enter your role: ")
    age = int(input("Enter your age: "))
    gender = input("Enter your gender: ")

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Create a new User instance
    new_user = User(username=username, password=hashed_password, role=role, age=age, gender=gender)
    
    # Add the user to the session and commit
    session.add(new_user)
    session.commit()
    print("User created successfully.\n")

# Function to edit an existing user
def edit_user():
    username = input("Enter the username of the user you want to edit: ")
    user = session.query(User).filter_by(username=username).first()
    
    if user:
        print("User found. Choose a column to edit:")
        print("1. Username")
        print("2. Password")
        print("3. Role")
        print("4. Age")
        print("5. Gender")

        choice = int(input("Enter the number of the column you want to edit (1-5): "))
        
        if choice == 1:
            new_username = input("Enter the new username: ")
            user.username = new_username
            print("Username updated successfully.")
        elif choice == 2:
            new_password = input("Enter the new password: ")
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user.password = hashed_password
            print("Password updated successfully.")
        elif choice == 3:
            new_role = input("Enter the new role: ")
            user.role = new_role
            print("Role updated successfully.")
        elif choice == 4:
            new_age = int(input("Enter the new age: "))
            user.age = new_age
            print("Age updated successfully.")
        elif choice == 5:
            new_gender = input("Enter the new gender: ")
            user.gender = new_gender
            print("Gender updated successfully.")
        else:
            print("\nInvalid choice.")
        
        session.commit()
    else:
        print("User not found.")

# Function to delete a user
def delete_user():
    username = input("Enter the username of the user you want to delete: ")
    user = session.query(User).filter_by(username=username).first()
    
    if user:
        session.delete(user)
        session.commit()
        print("\nUser deleted successfully.")
    else:
        print("User not found.")

def login_user():
    while True:  # Loop until successful login or user decides to exit
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        user = session.query(User).filter_by(username=username).first()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            print("Successfully logged in.")
            print("User Data:")
            print(f"Username: {user.username}")
            print(f"Role: {user.role}")
            print(f"Age: {user.age}")
            print(f"Gender: {user.gender}")
            return True  # Return to indicate successful login
        else:
            print("\nInvalid credentials. Please try again.")
            continue

def main():
    logged_in = False  # Flag to track login state

    while True: 
        if not logged_in:
            print("\nChoose an action:")
            print("1. Create User")
            print("2. Edit User")
            print("3. Delete User")
            print("4. Login User")
            print("5. Exit")
            
            try:
                action = int(input("\nEnter the number of the action you want to perform (1-5): "))
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.\n")
                continue
            
            if action == 1:
                create_user()
            elif action == 2:
                edit_user()
            elif action == 3:
                delete_user()
            elif action == 4:
                logged_in = login_user()  # Update the login state
            elif action == 5:
                print("Exiting the application.")
                break
            else:
                print("Invalid action. Please choose a number between 1 and 5.\n")
        else:
            print("\nYou are already logged in. Choose an action:")
            print("1. Logout")
            print("2. Edit User")
            print("3. Delete User")
            print("4. Exit")
            
            try:
                action = int(input("\nEnter the number of the action you want to perform (1-4): "))
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 4.\n")
                continue

if __name__ == "__main__":
    Base.metadata.create_all(engine)  # Create tables if they don't exist
    main()

session.close()
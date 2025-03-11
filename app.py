from flask import Flask
from model import db


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

# Creates database tables
with app.app_context():
    db.create_all()



if __name__ == '__main__':
    app.run(debug=True)

   
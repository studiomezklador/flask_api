from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from boot import basedir

app = Flask(__name__)

db_file = basedir + '/data/api.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:/// ' + db_file

db = SQLAlchemy(app)


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    company = db.Column(db.String(100), index=True)
    email = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return '<Customer {}>'.format(self.name)

    def __str__(self):
        return self.name

if __name__ == '__main__':
    pass

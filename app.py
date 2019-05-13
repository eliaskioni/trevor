from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    addresses = db.relationship('Address', backref='user', lazy=False)


@app.route('/')
def hello_world():
    address = Address(name="Kioni")
    address2 = Address(name="James")
    user = User(name="Flask")
    user.addresses.append(address)
    user.addresses.append(address2)
    db.session.add(user)
    db.session.commit()
    users = [{'name': user.name, 'id': user.id} for user in  User.query.all()]
    return render_template('hello.html', name='Elias', users=users)


if __name__ == '__main__':
    app.run()

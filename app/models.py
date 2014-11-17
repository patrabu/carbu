# -*- coding: utf-8 -*

from app import app, db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(64))

    def get_id(self):
        return unicode(self.id)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # Valid token but expired
        except BadSignature:
            return None # Invalid token
        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return '<User %r>' % self.username


class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), index = True)
    description = db.Column(db.String(256), index = False)
    refills = db.relationship('Refill', backref = 'car', lazy = 'dynamic')

    def get_id(self):
        return unicode(self.id)

    def last_refills(self):
        return Refill.query.limit(LAST_REFILLS).order_by(Refill.timestamp.desc())

    def __repr__(self):
        return '<Car %r>' % self.name

class Refill(db.Model):
    __tablename__ = 'refills'
    id = db.Column(db.Integer, primary_key = True)
    datetime = db.Column(db.DateTime)
    quantity = db.Column(db.Float)
    price = db.Column(db.Float)
    mileage = db.Column(db.Integer)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))

    def get_id(self):
        return unicode(self.id)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'       : self.id,
           'datetime' : self.datetime,
           'price'    : self.price,
           'quantity' : self.quantity,
           'mileage'  : self.mileage,
           'car_id'   : self.car.id
       }

    def __repr__(self):
        return '<Refill %r>' % self.mileage

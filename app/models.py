from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.sql import func
from sqlalchemy.orm import backref
from datetime import datetime
import time

db = SQLAlchemy()


class BaseModel(db.Model):
    print_filter = ()
    to_json_filter = ()

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
            if column not in self.print_filter
        })

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def json(self):
        return {
            column: value
            if not isinstance(value, datetime) else time.mktime(value.timetuple())
            for column, value in self._to_dict().items()
            if column not in self.to_json_filter
        }

    def _to_dict(self):
        return {
            column.key: getattr(self, column.key)
            for column in inspect(self.__class__).attrs
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def to_naira(value):
        return value/100


class User(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    msisdn = db.Column(db.String(15), nullable=False, unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())


class Wallet(BaseModel):
    __tablename__ = 'wallets'

    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    balance = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    user = db.relationship('User', backref=backref('wallet', uselist=False))


class Funding(BaseModel):
    __tablename__ = 'funding'

    id = db.Column(db.Integer(), primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'), nullable=False)
    mode = db.Column(db.String(255), default='paystack')
    amount = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
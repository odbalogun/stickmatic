from app import db
from sqlalchemy import inspect
from sqlalchemy.sql import func
from sqlalchemy.orm import backref
from datetime import datetime
from .utils import msisdn_formatter
import time
import uuid


DEPOSIT_STATUS = ['Pending', 'Paid', 'Failed Payment']


class BaseModel(db.Model):
    __abstract__ = True

    print_filter = ()
    to_json_filter = ()

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
    _msisdn = db.Column(db.String(15), nullable=False, unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    @property
    def msisdn(self):
        return self._msisdn

    @msisdn.setter
    def msisdn(self, value):
        self._msisdn = msisdn_formatter(value)

    @property
    def purchase_history(self):
        purchase_list = []
        for x in self.wallet.purchase_history:
            purchase_list.append(x.json)
        return purchase_list

    @property
    def identity_email(self):
        if self.email:
            return self.email
        return f"{self.msisdn}@barillo.net"


class Wallet(BaseModel):
    __tablename__ = 'wallets'

    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    balance = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    user = db.relationship('User', backref=backref('wallet', uselist=False))

    def __init__(self, **kwargs):
        if not kwargs.get(uuid):
            # generate wallet uuid
            self.uuid = str(uuid.uuid4()).rsplit('-', 1)[0]
        super().__init__(**kwargs)


class Funding(BaseModel):
    __tablename__ = 'funding'

    id = db.Column(db.Integer(), primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'), nullable=False)
    mode = db.Column(db.String(255), default='paystack')
    amount = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    wallet = db.relationship('Wallet', backref='funding_history')


class PurchaseHistory(BaseModel):
    __tablename__ = 'purchase_history'

    id = db.Column(db.Integer(), primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'), nullable=False)
    products = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, default=0)
    wallet_balance = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    wallet = db.relationship('Wallet', backref='purchase_history')


class DepositTransaction(BaseModel):
    __tablename__ = 'deposit_transactions'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Integer, default=0)
    mode = db.Column(db.String(255), default='paystack')
    # 0 for pending - 1 for paid - 2 for failure
    status = db.Column(db.Integer, default=0)
    txn_reference = db.Column(db.String(50), nullable=True)
    note = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    user = db.relationship('User', backref=backref('deposits', uselist=False))

    @property
    def status_label(self):
        return DEPOSIT_STATUS[self.status]
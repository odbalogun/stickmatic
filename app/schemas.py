from app import ma
from app.models import User, Wallet, Funding
from marshmallow import fields, post_load


class FundingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Funding


class WalletSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Wallet
        include_fk = True

    funding_history = fields.Nested(FundingSchema, many=True)

    @post_load
    def make_object(self, data, **kwargs):
        return Wallet(**data)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        exclude = ['_msisdn']
        readonly = ['id', 'wallet']

    msisdn = fields.String(required=True)
    wallet = fields.Nested(WalletSchema(only=("id", "uuid", "balance")))

    @post_load
    def make_object(self, data, **kwargs):
        return User(**data)

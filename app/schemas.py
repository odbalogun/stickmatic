from app import ma
from app.models import User, Wallet


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True


class WalletSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Wallet
        include_fk = True

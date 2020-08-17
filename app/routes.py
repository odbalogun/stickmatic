from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from .schemas import UserSchema, WalletSchema
from .models import db, User, Wallet, Funding, PurchaseHistory
from .utils import response_error, msisdn_formatter

blueprint = Blueprint("api", __name__)


@blueprint.route('/users', methods=['GET', 'POST'])
def users_endpoint():
    if request.method == 'GET':
        users_schema = UserSchema(many=True)
        return jsonify(users_schema.dump(User.query.all()))
    data = request.get_json(force=True)
    if not data.get('msisdn'):
        return response_error(400, "Please provide an msisdn")
    schema = UserSchema()
    user = schema.load(data)

    try:
        user.wallet = Wallet()
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return response_error(409, "This msisdn already exists", 409)

    return jsonify(schema.dump(user)), 201


@blueprint.route('/users/<int:user_id>', methods=['GET', 'PUT'])
def user_endpoint(user_id):
    # get user
    msisdn = msisdn_formatter(user_id)
    user = User.query.filter(or_(User.id == user_id, User._msisdn == msisdn)).first()

    if not user:
        return response_error(404, "User not found", 404)

    schema = UserSchema()
    if request.method == 'GET':
        return jsonify(schema.dump(user)), 200

    # update user
    data = request.get_json(force=True)

    if 'msisdn' in data.keys() or 'id' in data.keys():
        return response_error(400, "Bad request. Neither msisdn or id can be updated")

    for k, v in data.items():
        setattr(user, k, v)
    user.save()

    return jsonify(schema.dump(user)), 200


@blueprint.route('/wallets', methods=['GET'])
def wallets_endpoint():
    schema = WalletSchema(many=True)
    return jsonify(schema.dump(Wallet.query.all()))


@blueprint.route('/wallets/<wallet_id>', methods=['GET'])
def wallet_endpoint(wallet_id):
    wallet = Wallet.query.filter(or_(Wallet.id == wallet_id, Wallet.uuid == wallet_id)).one_or_none()
    if not wallet:
        return response_error(404, "Wallet not found", 404)
    schema = WalletSchema()
    return jsonify(schema.dump(wallet))


@blueprint.route('/wallets/<wallet_id>/deposit', methods=['POST'])
def deposit_endpoint(wallet_id):
    wallet = Wallet.query.filter(or_(Wallet.id == wallet_id, Wallet.uuid == wallet_id)).one_or_none()
    if not wallet:
        return response_error(404, "Wallet not found", 404)

    data = request.get_json(force=True)
    if 'mode' not in data.keys() or 'amount' not in data.keys():
        return response_error(400, "Bad request. Mode and amount must be provided")

    wallet.funding_history.append(Funding(mode=data.get('mode'), amount=data.get('amount')))
    wallet.balance += data.get('amount')
    wallet.save()

    schema = WalletSchema()
    return jsonify(schema.dump(wallet))


@blueprint.route('/wallets/<wallet_id>/purchase', methods=['POST'])
def purchase_endpoint(wallet_id):
    wallet = Wallet.query.filter(or_(Wallet.id == wallet_id, Wallet.uuid == wallet_id)).one_or_none()
    if not wallet:
        return response_error(404, "Wallet not found", 404)

    data = request.get_json(force=True)
    if 'products' not in data.keys() or 'price' not in data.keys():
        return response_error(400, "Bad request. Products and price must be provided")

    if data.get('price') > wallet.balance:
        return response_error(400, "Bad request. Insufficient funds in wallet")

    wallet.balance -= data.get('price')
    wallet.purchase_history.append(PurchaseHistory(price=data.get('price'), wallet_balance=wallet.balance,
                                                   products=data.get('products')))
    wallet.save()
    schema = WalletSchema()
    return jsonify(schema.dump(wallet))
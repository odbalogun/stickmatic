from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from .schemas import UserSchema, WalletSchema
from .models import db, User, Wallet
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


@blueprint.route('/users/<int:user_id>', methods=['PUT'])
def user_endpoint(user_id):
    # get user
    user = User.query.get(user_id)

    if not user:
        return response_error(404, "User not found", 404)

    # update user
    data = request.get_json(force=True)

    if 'msisdn' in data.keys() or 'id' in data.keys():
        return response_error(400, "Bad request. Neither msisdn or id can be updated")

    for k, v in data.items():
        setattr(user, k, v)
    user.save()

    schema = UserSchema()
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

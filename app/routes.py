from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from stickmatic import app
from .schemas import UserSchema
from .models import db, User
from .utils import response_error, msisdn_formatter

blueprint = Blueprint("api", __name__)


@app.route('/users', methods=['GET', 'POST'])
def users_endpoint():
    if request.method == 'GET':
        users_schema = UserSchema(many=True)
        return users_schema.dump(User.query.all())
    data = {k.lower(): v for k, v in request.get_json().items()}
    if not data.get('msisdn'):
        return response_error(400, "Please provide an msisdn")
    schema = UserSchema()
    user = schema.load(data)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return response_error(409, "This msisdn already exists", 409)

    return schema.dump(user)
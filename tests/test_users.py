import json
from app.schemas import UserSchema
from app.models import User


def test_retrieve_users(client, init_database):
    response = client.get('/api/users')

    assert response.status_code == 200
    data = response.json
    assert len(data) == 2


def test_for_user_creation(client, init_database):
    payload = dict(msisdn="09060801111")
    response = client.post('/api/users', data=json.dumps(payload))
    assert response.status_code == 201
    data = response.json
    # check that msisdn is formatted correctly
    assert data.get('msisdn') == '2349060801111'
    # check that wallet was created
    assert data.get('wallet') is not None


def test_for_duplicate_user_msisdn(client, init_database):
    # count users in db
    count = len(User.query.all())

    payload = dict(msisdn="09060010102")
    response = client.post('/api/users', data=json.dumps(payload))

    assert response.status_code == 409
    # check that no of users in db has not changed
    assert len(User.query.all()) == count


def test_user_can_be_updated(client, init_database):
    payload = dict(first_name="Joyner", last_name="Lucas")
    response = client.put('/api/users/1', data=json.dumps(payload))

    assert response.status_code == 201
    # check that first_name and last_name have been updated
    user = User.query.get(1)
    assert user.first_name == "Joyner"
    assert user.last_name == "Lucas"


def test_user_id_and_msisdn_can_not_be_updated(client, init_database):
    payload = dict(user_id=3, msisdn="09060708080")
    response = client.put('/api/users/1', data=json.dumps(payload))

    assert response.status_code == 400


def test_cannot_update_nonexistent_user(client, init_database):
    payload = dict(first_name="Joyner", last_name="Lucas")
    response = client.put('/api/users/10000', data=json.dumps(payload))

    assert response.status_code == 404
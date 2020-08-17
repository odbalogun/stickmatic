import pytest
from app import create_app
from app.models import db, User, Wallet
from config import TestConfig


@pytest.fixture
def app():
    yield create_app(TestConfig)


@pytest.fixture(scope='module')
def client():
    flask_app = create_app(TestConfig)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    user1 = User(msisdn='2349060010101')
    user1.wallet = Wallet()
    user2 = User(msisdn='2349060010102')
    user2.wallet = Wallet()
    db.session.add(user1)
    db.session.add(user2)

    # Commit the changes for the users
    db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()
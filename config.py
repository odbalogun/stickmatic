import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1srMQajnG7Zkt9z2RcYD'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'stickmatic.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('DEBUG') or True
    ENV = os.environ.get('ENV') or 'development'
    TESTING = os.environ.get('TESTING') or True
    PAYSTACK_KEY = os.environ.get('PAYSTACK_KEY')


class TestConfig(Config):
    ENV = 'testing'
    BCRYPT_LOG_ROUNDS = 3
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


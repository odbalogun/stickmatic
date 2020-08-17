import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1srMQajnG7Zkt9z2RcYD'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'stickmatic.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    ENV = 'development'
    TESTING = True
    FLASK_DEBUG = 1


class TestConfig(object):
    TESTING = True
    DEBUG = True
    ENV = 'testing'
    BCRYPT_LOG_ROUNDS = 3
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(object):
    DEBUG = False
    ENV = 'production'
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1srMQajnG7Zkt9z2RcYD'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'stickmatic.db')

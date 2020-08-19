from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from config import Config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from app.routes import blueprint as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.views import blueprint as page_bp
    app.register_blueprint(page_bp)

    return app


from app import models

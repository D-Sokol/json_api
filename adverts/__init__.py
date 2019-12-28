from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_cls=Config):
    app = Flask(__name__)
    app.config.from_object(config_cls)
    db.init_app(app)
    migrate.init_app(app)
    return app

app = create_app()


from . import routes

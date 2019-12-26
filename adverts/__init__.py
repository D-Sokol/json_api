from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    migrate.init_app(app)
    return app

app = create_app()


from . import routes

# TODO: create tables with migrations
with app.app_context():
    db.create_all()

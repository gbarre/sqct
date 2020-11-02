import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig


db = SQLAlchemy()

from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

ma = Marshmallow()

basedir = os.path.abspath(os.path.dirname(__file__))
migrate = Migrate()


def create_app():

    connex_app = connexion.App(
        __name__,
        specification_dir=os.path.join(basedir, 'spec'),
    )
    connex_app.add_api(
        'openapi.yml',
        strict_validation=True,
        validate_responses=True
    )
    # connex_app.run(port=5000)

    app = connex_app.app

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqct.db'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(DevelopmentConfig)

    # Initializing app extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    return connex_app

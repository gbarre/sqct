import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
ma = Marshmallow()

app =  connexion.App(__name__, specification_dir=os.path.join(basedir, 'spec'))
app.add_api('openapi.yml', strict_validation=True,validate_responses=True)
app.run(port=5000)
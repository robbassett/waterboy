# config.py

import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'waterboy.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["ASSETS_ROOT"] = os.getenv('ASSETS_ROOT', '/static/assets')

db = SQLAlchemy(app)
ma = Marshmallow(app)
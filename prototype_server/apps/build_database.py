# build_database

# build_database.py

from datetime import datetime
from config import app, db
from models import Measure

MEASURES = [
    {"measure_name":"Soil Moisture","measure_units":"percent"},
    {"measure_name":"Soil Moisture Raw","measure_units":"??"},
    {"measure_name":"Light","measure_units":"lux"}
]

with app.app_context():
    db.drop_all()
    db.create_all()
    for data in MEASURES:
        new_measure = Measure(**data)
        db.session.add(new_measure)
    db.session.commit()
# plants.py

from flask import abort, make_response
from config import db
from models import Plant, plant_schema, plants_schema

def read_all():
    plants = Plant.query.all()
    return plants_schema.dump(plants)

def create(plant):
    name = plant.get("plant_name")
    existing_plant = Plant.query.filter(Plant.plant_name == name).one_or_none()

    if existing_plant is None:
        new_plant = plant_schema.load(plant, session=db.session)
        db.session.add(new_plant)
        db.session.commit()
        return plant_schema.dump(new_plant), 201
    else:
        abort(406,f"Plant with name {name} already exists")
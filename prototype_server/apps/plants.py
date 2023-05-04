# plants.py

from flask import abort, make_response
from config import db
from models import Plant, plant_schema, plants_schema

def read_all():
    plants = Plant.query.all()
    return plants_schema.dump(plants)

def get(plant_name):
    plant = Plant.query.filter(Plant.plant_name == plant_name).one_or_none()
    if plant:
        return plant_schema.dump(plant), 200
    else:
        abort(404,f"Plant with name {plant_name} not found")

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

def update(plant_name, plant):
    existing_plant = Plant.query.filter(Plant.plant_name == plant_name).one_or_none()

    if existing_plant:
        update_plant = plant_schema.load(plant, session=db.session)
        if update_plant.plant_name is not None:
            existing_plant.plant_name = update_plant.plant_name
        if update_plant.genus is not None:
            existing_plant.genus = update_plant.genus
        if update_plant.species is not None:
            existing_plant.species = update_plant.species
        if update_plant.pump_time is not None:
            existing_plant.pump_time = update_plant.pump_time
        if update_plant.dry_hours is not None:
            existing_plant.dry_hours = update_plant.dry_hours
        if update_plant.image_loc is not None:
            existing_plant.image_loc = update_plant.image_loc

        print(existing_plant)

        db.session.merge(existing_plant)
        db.session.commit()
        return plant_schema.dump(existing_plant), 201
    else:
        abort(404,f"Plant with last name {plant_name} not found")

def delete(plant_name):
    existing_plant = Plant.query.filter(Plant.plant_name == plant_name).one_or_none()

    if existing_plant:
        db.session.delete(existing_plant)
        db.session.commit()
        return make_response(f"{plant_name} sucessfully deleted", 204)
    else:
        abort(404,f"Person with last name {plant_name} not found")
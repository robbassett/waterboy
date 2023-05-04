# profile.py

from config import db
from models import Plant, Measure, Value, value_schema
import json

def get_profile_info(plant_name):
    plant = Plant.query.filter(Plant.plant_name == plant_name).one_or_none()
    genus = plant.genus
    species = plant.species
    dry_hours = plant.dry_hours
    pump_time = plant.pump_time
    image_loc = plant.image_loc

    return json.dumps({
        "genus":genus,
        "species":species,
        "dry_hours":dry_hours,
        "pump_time":pump_time,
        "image_loc":image_loc
    })


    
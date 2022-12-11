from flask import abort
from config import db
from models import Plant, Measure, value_schema
from datetime import datetime

def create(value):
    plant_name = value.get("plant_name")
    plant = Plant.query.filter(Plant.plant_name == plant_name).one_or_none()
    if plant is None:
        abort(404, f"Plant with name {plant_name} not found.")

    measure_name = value.get("measure_name")
    measure = Measure.query.filter(Measure.measure_name == measure_name).one_or_none()
    if measure is None:
        abort(404, f"Measure with name {measure_name} not found")

    value_dic = {
        'measure_id':measure.measure_id,
        'plant_id':plant.plant_id,
        'value':value.get("value"),
        'timestamp':datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
    }

    new_value = value_schema.load(value_dic, session=db.session)
    plant.traces.append(new_value)
    db.session.commit()

    return value_schema.dump(new_value),201
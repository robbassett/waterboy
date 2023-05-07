from flask import abort
from config import db
from models import Plant, Measure, Value, value_schema
from datetime import datetime
import numpy as np

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

    response = value_schema.dump(new_value)
    response["pump"] = False
    if value.get("measure_name") == "Soil Moisture Raw":
        values = Value.query.filter(
            (Value.plant_id == plant.plant_id)&(Value.measure_id == measure.measure_id)
        ).all()
        x2 = np.array([value.timestamp for value in values])
        y2 = np.array([value.value for value in values])

        order = np.argsort(x2)[::-1]
        x2 = x2[order]
        y2 = y2[order]

        for i,y in enumerate(y2):
            if y < 45000:
                break

        print(datetime.now()-x2[i])
        response["pump_time"] = plant.pump_time
        try:
            if (datetime.now()-x2[i]).total_seconds()/3600. > plant.dry_hours:
                response["pump"] = True
        except:
            pass
        print(response)

    return response,201
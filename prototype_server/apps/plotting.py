# plotting.py

import plotly.graph_objects as go
import plotly
import json
from datetime import datetime,timedelta
import numpy as np

from config import db
from models import Plant, Measure, Value, value_schema

def get_trace(plant_name,measure_name='Soil Moisture',db=db):
    plant = Plant.query.filter(Plant.plant_name == plant_name).one_or_none()
    plant_id = plant.plant_id

    measure = Measure.query.filter(Measure.measure_name == measure_name).one_or_none()
    measure_id = measure.measure_id

    values = Value.query.filter(
        (Value.plant_id == plant_id)&(Value.measure_id == measure_id)
    ).all()

    x = np.array([value.timestamp for value in values])
    y = np.array([value.value for value in values])

    measure = Measure.query.filter(Measure.measure_name == "Light").one_or_none()
    measure_id = measure.measure_id

    values = Value.query.filter(
        (Value.plant_id == plant_id)&(Value.measure_id == measure_id)
    ).all()

    y2 = np.array([value.value for value in values])

    xend = x.max()+timedelta(minutes=5)
    xstart = xend-timedelta(hours=48)
    tsel = list(np.where(x >= xstart)[0])
    x = x[tsel]
    y = y[tsel]

    out = json.dumps([list(y),list(y2)])
    return out
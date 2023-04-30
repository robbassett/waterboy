# plotting.py

import plotly.graph_objects as go
import plotly
import json
from datetime import datetime,timedelta
import numpy as np

from config import db
from models import Plant, Measure, Value, value_schema

def get_measure_trace(plant_id,measure_name,time_period=48):
    measure = Measure.query.filter(Measure.measure_name == measure_name).one_or_none()
    measure_id = measure.measure_id

    values = Value.query.filter(
        (Value.plant_id == plant_id)&(Value.measure_id == measure_id)
    )

    x = np.array([value.timestamp for value in values])
    y = np.array([value.value for value in values])

    xend = x.max()+timedelta(minutes=5)
    xstart = xend-timedelta(hours=time_period)
    tsel = list(np.where(x >= xstart)[0])
    x = x[tsel]
    y = y[tsel]
    x = [(_-xend).total_seconds()/3600. for _ in x]

    return x,y

def output_plotly(plant_name,raw=False):
    plant = Plant.query.filter(Plant.plant_name == plant_name).one_or_none()
    plant_id = plant.plant_id

    rstr = " Raw" if raw else ""

    traces = {
        measure:get_measure_trace(plant_id,measure) for measure in [
            "Soil Moisture"+rstr,"Light"+rstr
        ]
    }

    F = go.Figure()
    for k,trace in traces.items():
        F.add_trace(go.Scatter(
            x=trace[0],
            y=trace[1],
            name=k,
            line={'shape': 'spline', 'smoothing': 0.5}
        ))

    return json.dumps(F, cls=plotly.utils.PlotlyJSONEncoder)

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

    x2 = np.array([value.timestamp for value in values])
    y2 = np.array([value.value for value in values])

    xend = x.max()+timedelta(minutes=5)
    xstart = xend-timedelta(hours=48)
    tsel = list(np.where(x >= xstart)[0])
    x = x[tsel]
    y = y[tsel]
    xo = [(_-xend).total_seconds()/3600. for _ in x]


    xend = x2.max()+timedelta(minutes=5)
    xstart = xend-timedelta(hours=48)
    tsel = list(np.where(x2 >= xstart)[0])
    x2 = x2[tsel]
    y2 = y2[tsel]

    x2o = [(_-xend).total_seconds()/3600. for _ in x2]

    yo = []
    for _x in x2o:
        print(np.abs(np.array(xo)-_x)*3600.)
        if np.abs((np.array(xo)-_x)*3600.).min() < 12:
            yo.append(y[np.argmin(np.abs((np.array(xo)-_x)))])
        else:
            yo.append('null')

    x2o = [datetime.strftime(_,"%d/%m/%y %H:%M:%S") for _ in x2]

    out = json.dumps([list(yo),list(y2),list(x2o)])
    return out
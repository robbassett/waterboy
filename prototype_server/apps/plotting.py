# plotting.py

from time import time
import plotly.graph_objects as go
import plotly
import json
from datetime import datetime,timedelta
import numpy as np

from config import db
from models import Plant, Measure, Value, value_schema

def get_measure_trace(plant_id,measure_name,time_period=4):
    measure = Measure.query.filter(Measure.measure_name == measure_name).one_or_none()
    measure_id = measure.measure_id

    values = Value.query.filter(
        (Value.plant_id == plant_id)&(Value.measure_id == measure_id)
    )

    x = np.array([value.timestamp for value in values])
    y = np.array([value.value for value in values])

    try:
        xend = x.max()+timedelta(minutes=5)
    except:
        return [],[],[]
    xstart = xend-timedelta(hours=time_period)
    tsel = list(np.where(x >= xstart)[0])
    x = x[tsel]
    y = y[tsel]

    c = "#2361ce" if "Soil" in measure_name else "#f0bc74"

    return x,y,c

def output_plotly(plant_name,raw=False,time_period=4):
    plant = Plant.query.filter(Plant.plant_name == plant_name).one_or_none()
    plant_id = plant.plant_id

    rstr = " Raw" if raw else ""

    traces = {
        measure:get_measure_trace(plant_id,measure,time_period=time_period) for measure in [
            "Soil Moisture"+rstr,"Light"+rstr,"Pump On"
        ]
    }

    F = go.Figure()
    F.add_hline(22.5,line_width=5,line_color="#000000",line_dash="dash")
    for k,trace in traces.items():
        if k != "Pump On":
            F.add_trace(go.Scatter(
                x=trace[0],
                y=trace[1],
                name=k,
                line={
                    'shape': 'spline', 
                    'smoothing': 0.7,
                    'color':trace[2],
                    'width':5
                },
                marker={
                    "size":15
                },
                fill='tozeroy',
            ))
        else:
            for x in trace[0]:
                F.add_vline(x=x, line_width=5,line_color="#2361ce")

    yax = "Reading" if raw else "Percent"

    F.update_layout(
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="center",
            x=0.5
        ),
        paper_bgcolor="#D1D5DB",
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        legend_orientation="h",
        font=dict(
            family="Arial Black",
            size=18,
        ),
        yaxis_title=yax,
    )

    F.update_xaxes(
        showgrid=True, 
        showline=True,
        gridwidth=3, 
        linewidth=3,
        gridcolor='White',
        linecolor='#1F2937',
        mirror=True
    )

    F.update_yaxes(
        showgrid=True, 
        showline=True,
        gridwidth=3, 
        linewidth=3,
        gridcolor='White',
        linecolor='#1F2937',
        mirror=True
    )

    return json.dumps(F, cls=plotly.utils.PlotlyJSONEncoder)

def get_trace(plant_name,measure_name='Soil Moisture',db=db):
    plant = Plant.query.filter(Plant.plant_name == plant_name).one_or_none()
    plant_id = plant.plant_id

    measure = Measure.query.filter(Measure.measure_name == measure_name).one_or_none()
    measure_id = measure.measure_id

    values = Value.query.filter(
        (Value.plant_id == plant_id)&(Value.measure_id == measure_id)
    ).all()

    y = np.array([value.value for value in values])

    measure = Measure.query.filter(Measure.measure_name == "Light").one_or_none()
    measure_id = measure.measure_id

    values = Value.query.filter(
        (Value.plant_id == plant_id)&(Value.measure_id == measure_id)
    ).all()

    y2 = np.array([value.value for value in values])

    out = json.dumps([list(y),list(y2)])
    return out
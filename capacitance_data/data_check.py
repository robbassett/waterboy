import sqlalchemy
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

engine = sqlalchemy.create_engine("sqlite:///waterboy_cap_probe.db")

eric = pd.read_sql("SELECT timestamp,value,V.measure_id FROM Value AS V JOIN Plant as P ON V.plant_id=P.plant_id JOIN Measure as M ON V.measure_id=M.measure_id\
    WHERE V.plant_id=1",engine)

lily = pd.read_sql("SELECT timestamp,value,V.measure_id FROM Value AS V JOIN Plant as P ON V.plant_id=P.plant_id JOIN Measure as M ON V.measure_id=M.measure_id\
    WHERE V.plant_id=2",engine)

F = plt.figure(figsize=(16,14))
lbs = ['Soil Moisture %','Soil Moisture Raw','Light %']

for i in [1,2,3]:
    ax = F.add_subplot(3,1,i)

    x = np.array([dt.datetime.strptime(_,"%Y-%m-%d %H:%M:%S.%f") for _ in eric[eric['measure_id'] == i]['timestamp']])
    y = np.array(eric[eric['measure_id'] == i]['value'])
    t = np.where(x > dt.datetime.strptime("2023-03-13","%Y-%m-%d"))[0]
    ax.plot(x[t],y[t],label='Erik')

    x = np.array([dt.datetime.strptime(_,"%Y-%m-%d %H:%M:%S.%f") for _ in lily[lily['measure_id'] == i]['timestamp']])
    y = np.array(lily[lily['measure_id'] == i]['value'])
    t = np.where(x > dt.datetime.strptime("2023-03-13","%Y-%m-%d"))[0]
    ax.plot(x[t],y[t],label='Lily')
    if i == 1:
        ax.legend(loc='upper center',ncol=2)
    ax.set_ylabel(lbs[i-1])

plt.savefig('data_check.png')
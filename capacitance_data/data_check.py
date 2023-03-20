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

F = plt.figure()
ax = F.add_subplot(111)

x = np.array([dt.datetime.strptime(_,"%Y-%m-%d %H:%M:%S.%f") for _ in eric[eric['measure_id'] == 1]['timestamp']])
y = np.array(eric[eric['measure_id'] == 1]['value'])
t = np.where(x > dt.datetime.strptime("2023-03-13","%Y-%m-%d"))[0]
ax.plot(x[t],y[t])

j = np.argmin(y[t])
i = np.argmax(y[t])
print(x[t[j]])
print(x[t[i]])

x = np.array([dt.datetime.strptime(_,"%Y-%m-%d %H:%M:%S.%f") for _ in lily[lily['measure_id'] == 1]['timestamp']])
y = np.array(lily[lily['measure_id'] == 1]['value'])
t = np.where(x > dt.datetime.strptime("2023-03-13","%Y-%m-%d"))[0]
ax.plot(x[t],y[t])

plt.show()
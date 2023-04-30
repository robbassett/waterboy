# build_database.py

from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    ForeignKey,
    ForeignKeyConstraint,
    String,
    DateTime,
    Boolean,
)

from sqlalchemy.schema import Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import datetime as dt

# anyone out there? change this is you feel like running...
db_url = "sqlite:////Users/robertbassett/Desktop/repos/waterboy/prototype_server/mock_db/waterboy.db"
engine = create_engine(db_url)
Base = declarative_base()

class Measure(Base):
    __tablename__ = "measure"

    measure_id = Column(Integer,primary_key=True)
    measure_name = Column(String,nullable=False)
    measure_units = Column(String,nullable=False)

class Plant(Base):
    __tablename__ = "plant"

    plant_id = Column(Integer,Sequence("plant_id_sequence"),primary_key=True)
    plant_name = Column(String,unique=True,nullable=False)
    genus = Column(String)
    species = Column(String)
    dry_hours = Column(Float)
    pump_time = Column(Float)

class Value(Base):
    __tablename__ = "value"

    value_id = Column(Integer, Sequence("value_id_sequence") ,primary_key=True)
    measure_id = Column(Integer, nullable=False)
    plant_id = Column(Integer, nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=dt.datetime.now())

    __table_args__ = (
        ForeignKeyConstraint([measure_id],[Measure.measure_id]),
        ForeignKeyConstraint([plant_id],[Plant.plant_id]),
    )

Base.metadata.create_all(bind=engine)

vals = [25000]*3 + [50000]*12

def pval(raw,maxval=51000,minval=24400):
    
    normed = (raw-minval)/(maxval-minval)
    return 100.*(1.-normed)

def generate_dummy_data(
    plant_names = ["Jimmy","Johnny","Jerry"],
    plant_genus = ["Googly","Moogly","Halatosis"],
    plant_species = ["Tree","Shrub","Mushroomus"],
    plant_drydays = [1,2,3],
    plant_pumptime = [2,2,2],
    nval = 15, timedelt = 2
):

    import numpy as np

    MEASURES = [
        {"measure_name":"Soil Moisture","measure_units":"percent"},
        {"measure_name":"Soil Moisture Raw","measure_units":"??"},
        {"measure_name":"Light","measure_units":"percent"},
        {"measure_name":"Light Raw","measure_units":"lux"}
    ]

    with Session(engine) as session:
        for data in MEASURES:
            measure = Measure(**data)
            session.add(measure)

        pid = 0
        for n,g,s,dd,pt in zip(plant_names,plant_genus,plant_species,plant_drydays,plant_pumptime):
            pid += 1
            pdat = {"plant_name":n,"genus":g,"species":s,"dry_hours":dd*24.,"pump_time":pt}
            plant = Plant(**pdat)
            session.add(plant)

            for _ in range(nval):
                ctime = dt.datetime.now() - dt.timedelta(hours=timedelt*(nval-(_+1)))
                for mid in [2]:
                    v = vals[_]
                    vdat = {
                        "measure_id":mid,"plant_id":pid,"value":v,"timestamp":ctime
                    }
                    val = Value(**vdat)
                    session.add(val)

                    vd2 = {
                        "measure_id":1,"plant_id":pid,"value":pval(v),"timestamp":ctime
                    }
                    val2 = Value(**vd2)
                    session.add(val2)

                    vd3 = {
                        "measure_id":3,"plant_id":pid,"value":np.random.uniform(10,100),"timestamp":ctime
                    }
                    val3 = Value(**vd3)
                    session.add(val3)


        session.commit()

    return engine

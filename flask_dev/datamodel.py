
from trace import Trace
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    ForeignKey,
    ForeignKeyConstraint,
    String,
    DateTime,
    Boolean
)

from sqlalchemy.schema import Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Plants(Base):
    __tablename__ = 'Plants'

    Name = Column(String, primary_key=True)
    Genus = Column(String)
    Species = Column(String)

class TraceTypes(Base):
    __tablename__ = "TraceTypes"

    Trace_ID = Column(Integer,Sequence("trace_type_seq"), primary_key=True)
    Trace_Name = Column(String,nullable=False)
    Trace_Units = Column(String,nullable=False)

class TraceData(Base):
    __tablename__ = 'TraceData'

    uid = Column(Integer,Sequence("trace_id_seq"), primary_key=True)
    Trace_ID = Column(Integer)
    Time = Column(DateTime)
    Value = Column(Float)

    __table_args__ = (
        ForeignKeyConstraint([Trace_ID],[TraceTypes.Trace_ID]),{}
    )

from sqlalchemy import create_engine

# db_url = "sqlite:////Users/robertbassett/Desktop/repos/waterboy/flask_dev/waterboy_db.db"
# engine = create_engine(db_url)
# Base.metadata.create_all(bind=engine)

# from sqlalchemy.orm import sessionmaker
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

# trace = TraceTypes(Trace_Name='Soil Moisture',Trace_Units='wfv')
# session.add(trace)
# session.commit()
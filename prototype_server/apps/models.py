# models.py

from datetime import datetime
from marshmallow_sqlalchemy import fields
from config import db, ma

class Measure(db.Model):
    __tablename__ = "measure"
    measure_id = db.Column(db.Integer, primary_key=True)
    measure_name = db.Column(db.String, nullable=False)
    measure_units = db.Column(db.String, nullable=False)

class MeasureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Measure
        load_instance = True
        sqla_session = db.session

class Value(db.Model):
    __tablename__ = "value"
    value_id = db.Column(db.Integer, primary_key=True)
    measure_id = db.Column(db.Integer, db.ForeignKey("measure.measure_id"))
    plant_id = db.Column(db.Integer, db.ForeignKey("plant.plant_id"))
    value = db.Column(db.Float,nullable=False)
    timestamp = db.Column(db.DateTime,default=datetime.now())

class ValueSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Value
        load_instance = True
        sqla_session = db.session
        include_fk = True

class Plant(db.Model):
    __tablename__ = "plant"
    plant_id = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String,unique=True)
    genus = db.Column(db.String)
    species = db.Column(db.String)
    dry_hours = db.Column(db.Float)
    pump_time = db.Column(db.Float)
    image_loc = db.Column(db.String)
    traces = db.relationship(
        Value,
        backref="plant",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="asc(Value.timestamp)"
    )

class PlantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Plant
        load_instance = True
        sqla_session = db.session

measure_schema = MeasureSchema()
value_schema = ValueSchema()
plant_schema = PlantSchema()
plants_schema = PlantSchema(many=True)
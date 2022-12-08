from flask import Flask,jsonify,request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

from datamodel import Plants,TraceData

app = Flask(__name__)

db_url = "sqlite:////Users/robertbassett/Desktop/repos/waterboy/flask_dev/waterboy_db.db"
engine = create_engine(db_url)
DBSession = sessionmaker(bind=engine)
session = DBSession()

existing_plants = pd.read_sql("SELECT * FROM Plants",engine)

@app.route('/plant')
def add_plant():
    name = request.args.get('name')
    try:
        genus = request.args.get('genus')
    except:
        genus = None
    try:
        species = request.args.get('species')
    except:
        species = None

    if name in list(existing_plants['Name']):
        return "Plant Already Exists!"
    else:
        session.add(Plants(Name=name,Genus=genus,Species=species))
        session.commit()
        return f"{name} successfully added!"

@app.route('/query-example')
def query_example():
    # if key doesn't exist, returns None
    language = request.args.get('language')

    return '''<h1>The language value is: {}</h1>'''.format(language)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
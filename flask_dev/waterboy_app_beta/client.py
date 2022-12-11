# client.py

import requests as req

PLANT_NAME = "Sylvia"
GENUS = "Schefflera"
SPECIES = "Designer"
BASE_URL = "http://127.0.0.1:8000"

def startup(base_url=BASE_URL):
    r = req.get(base_url+'/api/plant/'+PLANT_NAME)
    if r.status_code == 404:
        body = {
            "plant_name":PLANT_NAME,
            "genus":GENUS,
            "species":SPECIES
        }
        r = req.post(base_url+'/api/plant',json=body)

def post_value(value,base_url=BASE_URL,measure_name="Soil Moisture"):
    body = {
        "plant_name":PLANT_NAME,
        "measure_name":measure_name,
        "value":value
    }
    r = req.post(base_url+'/api/trace',json=body)

if __name__ == "__main__":
    import numpy as np
    from time import sleep

    startup()
    while True:
        value = np.random.uniform(0,100)
        post_value(value)
        sleep(15)

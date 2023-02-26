# proto_client.py

# PROTOTYPE CLIENT WITH PICO (no onboard wifi)
# requires serial connection to pico with http
# requests handled by laptop

import requests as req
from talker import Talker

PLANT_NAME = 'Freddy'
GENUS = 'Plantius'
SPECIES = 'Maximus'
BASE_URL = "http://127.0.0.1:8000"

WAIT_TIME = 2700

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
    from time import sleep
    pico_coms = Talker()

    startup()
    while True:
        pico_coms.send('read_soil_sensor()')
        value = float(pico_coms.receive())
        post_value(value)

        pico_coms.send('read_light_sensor()')
        value = float(pico_coms.receive())
        post_value(value,measure_name="Light")

        sleep(WAIT_TIME)
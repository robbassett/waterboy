# main.py

# to be saved on raspberry pi pico w
from utime import sleep
from machine import ADC,Pin
import network
import urequests
import os
import ujson

with open('./config.json') as fp:
    config = ujson.load(fp)

if config['logging']:
    log_file = open("/pico_log.txt","a")
    os.dupterm(log_file)

print("Connecting to wifi...")

SSID = config['server']['ssid']
PASSWORD = config['server']['password']
BASE_URL = config['server']['base_url']
WLAN = network.WLAN(network.STA_IF)
WLAN.active(True)
WLAN.connect(SSID,PASSWORD)

while not WLAN.isconnected(): pass
print("Connected!")

WAIT_TIME = 10800
WAIT_TIME -= 1
PLANT_NAME = config['plant']['name']
GENUS = config['plant']['genus']
SPECIES = config['plant']['species']

soil_sensor = ADC(config['sensors']['soil_pin'])
light_sensor = ADC(config['sensors']['light_pin'])

def read_soil_sensor(maxval=65535,minval=30600):
    normed = (soil_sensor.read_u16()-minval)/(maxval-minval)
    return 100.*(1.-normed)

def read_light_sensor():
    return light_sensor.read_u16()

def startup(base_url=BASE_URL):
    r = urequests.get(base_url+'/api/plant/'+PLANT_NAME)
    if r.status_code == 404:
        body = {
            "plant_name":PLANT_NAME,
            "genus":GENUS,
            "species":SPECIES
        }
        r = urequests.post(base_url+'/api/plant',json=body)
        r.close()

def post_value(value,base_url=BASE_URL,measure_name="Soil Moisture"):
    body = {
        "plant_name":PLANT_NAME,
        "measure_name":measure_name,
        "value":value
    }
    r = urequests.post(base_url+'/api/trace',json=body)
    r.close()

led = Pin("LED", Pin.OUT)
print("Checking if plant in DB...")
startup()
print("Starting monitor...")
check_ss = True
while True:
    led.toggle()
<<<<<<< Updated upstream
    value = read_soil_sensor()
    post_value(value)
    print('soil value',value)
=======
    if check_ss:
        raw,value = read_soil_sensor()
        post_value(value)
        post_value(raw,measure_name="Soil Moisture Raw")
        check_ss = False
    else:
        check_ss = True
>>>>>>> Stashed changes
    value = read_light_sensor()
    post_value(value,measure_name="Light")
    print('light value',value)
    sleep(1)
    led.toggle()
    sleep(WAIT_TIME)


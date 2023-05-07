# main.py

# to be saved on raspberry pi pico w
from utime import sleep
from machine import ADC,Pin,PWM
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
PLANT_NAME = config['plant']['name'].replace(' ','_')
GENUS = config['plant']['genus']
SPECIES = config['plant']['species']
PUMP_TIME = config['plant']['pump_time']
DRY_HOURS = config['plant']['dry_hours']

soil_sensor = ADC(config['sensors']['soil_pin'])
light_sensor = ADC(config['sensors']['light_pin'])
water_pump = PWM(Pin(config['pump']['pin'],Pin.OUT))
water_pump.freq(config['pump']['freq'])
water_pump_duty = config['pump']['duty']

def read_soil_sensor(maxval=51000,minval=24400):
    raw = soil_sensor.read_u16()
    normed = (raw-minval)/(maxval-minval)
    return raw,100.*(1.-normed)

def read_light_sensor():
    raw = light_sensor.read_u16()
    return raw,raw/1e3

def run_pump(t):
    water_pump.duty_u16(water_pump_duty)
    sleep(t)
    water_pump.duty_u16(0)

def startup(base_url=BASE_URL):
    r = urequests.get(base_url+'/api/plant/'+PLANT_NAME)
    if r.status_code == 404:
        print("Adding new plant to db...")
        body = {
            "plant_name":PLANT_NAME,
            "genus":GENUS,
            "species":SPECIES,      
            "pump_time":PUMP_TIME,
            "dry_hours":DRY_HOURS
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
    return r

led = Pin("LED", Pin.OUT)
print("Checking if plant in DB...")
startup()
print("Starting monitor...")

while True:
    led.toggle()
    raw,value = read_soil_sensor()
    post_value(value)
    resp = post_value(raw,measure_name="Soil Moisture Raw")
    print(resp.json())

    if resp.json()["pump"]:
        run_pump(resp.json()["pump_time"])
        post_value(["pump_time"],measure_name="Pump On")

    raw,value = read_light_sensor()
    post_value(value,measure_name="Light")
    post_value(raw,measure_name="Light Raw")
    sleep(1)
    led.toggle()
    sleep(WAIT_TIME)

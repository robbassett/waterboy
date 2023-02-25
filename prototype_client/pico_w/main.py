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

WAIT_TIME = 30
PLANT_NAME = config['plant']['name']
GENUS = config['plant']['genus']
SPECIES = config['plant']['species']

soil_sensor = ADC(config['sensors']['soil_pin'])
light_sensor = ADC(config['sensors']['light_pin'])
water_pump = PWM(Pin(config['pump']['pin'],Pin.OUT))
water_pump.freq(config['pump']['freq'])
water_pump_duty = config['pump']['duty']
water_pump_time = config['pump']['ontime']

def read_soil_sensor(maxval=65535,minval=30600):
    raw = soil_sensor.read_u16()
    normed = (raw-minval)/(maxval-minval)
    return raw,100.*(1.-normed)

def read_light_sensor():
    return light_sensor.read_u16()

def run_pump():
    water_pump.duty_u16(water_pump_duty)
    sleep(water_pump_time)
    water_pump.duty_u16(0)

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
while True:
    led.toggle()
    raw,value = read_soil_sensor()
    post_value(value)
    value = read_light_sensor()
    post_value(value,measure_name="Light")
    sleep(1)
    led.toggle()
    sleep(WAIT_TIME)


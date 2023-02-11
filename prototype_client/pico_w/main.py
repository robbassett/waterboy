# main.py

# to be saved on raspberry pi pico w
from utime import sleep
from machine import ADC,Pin
import network
import urequests

SSID = "XXX"
PASSWORD = "XXX"
BASE_URL = "XXX"
WLAN = network.WLAN(network.STA_IF)
WLAN.active(True)
WLAN.connect(SSID,PASSWORD)

# Pause while device connects to WiFi
while not WLAN.isconnected(): pass

WAIT_TIME = 60
PLANT_NAME = 'Johnny'
GENUS = 'Hamburgerium'
SPECIES = 'Yummium'

# SOIL SENSOR ANALOG OUT
# TO PICO PIN 26
soil_sensor = ADC(26)

def read_soil_sensor(maxval=65535,minval=30600):
    normed = (soil_sensor.read_u16()-minval)/(maxval-minval)
    return 100.*(1.-normed)

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
startup()
while True:
    led.toggle()
    value = read_soil_sensor()
    post_value(value)
    sleep(2)
    led.toggle()
    sleep(WAIT_TIME)

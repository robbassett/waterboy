# main.py

# to be saved on raspberry pi pico w
from utime import sleep
from machine import ADC,Pin
import os
import ujson

with open('./config.json') as fp:
    config = ujson.load(fp)

if config['logging']:
    log_file = open("/pico_log.txt","a")
    os.dupterm(log_file)


WAIT_TIME = 30
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


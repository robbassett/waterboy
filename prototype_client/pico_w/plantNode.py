# plantNode.py

from utime import sleep
from machine import ADC,Pin,PWM
import network
import urequests
import os
import ujson

class plantNode():

    def __init__(
        self,
        config_file="config.json"
    ):
        with open(config_file) as fp:
            self.config = ujson.load(fp)

        if self.config['logging']:
            log_file = open("/pico_log.txt","a")
            os.dupterm(log_file)

        self.wait_time = 10800
        self.wait_time -= 1
        self.plantName = self.config['plant']['name'].replace(' ','%20')
        self.genus = self.config['plant']['genus']
        self.species = self.config['plant']['species']
        self.pumpTime = self.config['plant']['pump_time']
        self.dryHours = self.config['plant']['dry_hours']

        self.soil_sensor = ADC(self.config['sensors']['soil_pin'])
        self.light_sensor = ADC(self.config['sensors']['light_pin'])
        self.water_pump = PWM(Pin(self.config['pump']['pin'],Pin.OUT))
        self.water_pump.freq(self.config['pump']['freq'])
        self.water_pump_duty = self.config['pump']['duty']

        self.serverInfo = self.config['server']
        self.base_url = self.serverInfo['base_url']

        self.led = Pin("LED", Pin.OUT)

    def connect_to_wifi(self):
        print("Connecting to wifi...")

        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(
            self.serverInfo['ssid'],
            self.serverInfo['password']
        )

        while not self.wlan.isconnected(): pass
        print("Connected!")

    def startup(self):
        r = urequests.get(self.base_url+'/api/plant/'+self.plantName)
        if r.status_code == 404:
            print("Adding new plant to db...")
            body = {
                "plant_name":self.plantName,
                "genus":self.genus,
                "species":self.species,      
                "pump_time":self.pumpTime,
                "dry_hours":self.dryHours
            }
            r = urequests.post(self.base_url+'/api/plant',json=body)
            r.close()

    def disconnect_wifi(self):
        print("Disconnecting...")
        self.wlan.disconnect()
        print("WiFi disconnected.")

    def read_soil_sensor(self,maxval=51000,minval=24400):
        raw = self.soil_sensor.read_u16()
        normed = (raw-minval)/(maxval-minval)
        return raw,100.*(1.-normed)

    def read_light_sensor(self):
        raw = self.light_sensor.read_u16()
        return raw,raw/1e3

    def run_pump(self,t):
        self.water_pump.duty_u16(self.water_pump_duty)
        sleep(t)
        self.water_pump.duty_u16(0)

    def post_value(self,value,measure_name):
        body = {
            "plant_name":self.plantName,
            "measure_name":measure_name,
            "value":value
        }
        r = urequests.post(self.base_url+'/api/trace',json=body)
        return r

    def cycle(self):
        self.connect_to_wifi()
        self.led.toggle()

        raw,value = self.read_soil_sensor()
        self.post_value(value,"Soil Moisture")
        resp = self.post_value(raw,"Soil Moisture Raw")

        if resp.json()["pump"]:
            pumpTime = resp.json()["pump_time"]
            self.run_pump(pumpTime)
            self.post_value(pumpTime,"Pump On")

        raw,value = self.read_light_sensor()
        self.post_value(value,"Light")
        self.post_value(raw,"Light Raw")
        sleep(1)
        self.disconnect_wifi()
        self.led.toggle()

    def run(self):
        self.startup()
        while True:
            self.cycle()
            sleep(self.wait_time)
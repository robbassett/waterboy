# main.py

# to be saved on raspberry pi pico

from machine import ADC

# SOIL SENSOR ANALOG OUT
# TO PICO PIN 26
soil_sensor = ADC(26)

def read_soil_sensor(maxval=65535,minval=30600):
    normed = (soil_sensor.read_u16()-minval)/(maxval-minval)

    print(100.*(1.-normed))

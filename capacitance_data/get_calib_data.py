# get_calib_data.py
# To obtain 50 measurements for calibrating
# capacitive soil moisture sensor
# - - - - - - - - - - - - - - - - - - - - -
# Run once with output name set to "dry_data.txt"
# with probe in completely dry soil
# - - - - - - - - - - - - - - - - - - - - - 
# Run once with output name set to "wet_data.txt"
# with probe in completely wet soil
# - - - - - - - - - - - - - - - - - - - - -
# Run calibrate_sensor.py to produce graphs
# and get average calibration values for
# probes
# - - - - - - - - - - - - - - - - - - - - -
# Probe signal in ADC pin 26 of pi pico
# - - - - - - - - - - - - - - - - - - - - -

output_name = "dry_data.txt"
#output_name = "wet_data.txt"

from machine import ADC,Pin
from time import sleep

soil_sensor = ADC(Pin(26))
with open(output_name,'w') as fout:
    for _ in range(50):
        fout.write(soil_sensor.read_u16()+'\n')
        sleep(0.5)
    
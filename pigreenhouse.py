#!/usr/bin/env python
#
# PiGreenHouse
#
# Authors: Altran Gnomes, (c) 2017
#
import time
import json

from sensortag import cc2541
from sensortag import mcp3008
from sensortag import lampandpump


class Sensors(object):
    ''' Main class for the Sensors control '''

    def __init__(self):
        ''' Constructor '''
        self._cc2541  = cc2541.initialize_sensors()
        self._mcp3008 = mcp3008.initialize_sensors()

    def read_sensors(self):
        ''' Read all the sensors '''
        
        self._air_temp = self._cc2541.read_temperature()
        self._air_humidity = self._cc2541.read_humidity()
        self._ground_temp = self._cc2541.read_ground_temperature()

        self._soil_humidity = self._mcp3008.read_soil_humidity()
        self._light = self._mcp3008.read_lightsensor()
        self._water_alarm = self._mcp3008.read_wateralarm()

    def store_sensors(self):
        ''' Store sensors to file '''
        to_store = {}

        to_store['AirTemp'] = self._air_temp
        to_store['AirHumidity'] = self._air_humidity
        to_store['GroundTemp'] = self._ground_temp
        to_store['SoilHumidity'] = self._soil_humidity
        to_store['Light'] = self._light
        to_store['WaterAlarm'] = self._water_alarm

        with open('/tmp/sensorvalues.json', 'w') as aFile:
            aFile.write(json.dumps(to_store))

        print "* Stored values to /tmp/sensorvalues.json"
            
    def analysis(self):
        ''' Perform some analysis based on the sensor values '''

        self._mcp3008.handle_light(self._light)
        self._mcp3008.handle_pump(self._water_alarm, self._soil_humidity)


        

    
def main():
    ''' Main program of the PiGreenHouse '''
    print "* Initializing sensors..."
    sensors = Sensors()
    print "* Initializing sensors... done!"

    # Enter main loop
    while True:
        time.sleep(5)

        sensors.read_sensors()
        sensors.store_sensors()
        sensors.analysis()

        
        

    
    
    

if __name__ == '__main__':
    print "Welcome to PiGreenHouse!"
    main()

    

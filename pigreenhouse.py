#!/usr/bin/env python
#
# PiGreenHouse
#
# Authors: Altran Gnomes, (c) 2017
#
import time
import json
import os

from sensortag import cc2541
from sensortag import mcp3008
from sensortag import lampandpump
from sensortag import fan

class InputThread(threading.Thread):
    ''' Threading class used for checking input '''
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self.args)

def check_input_file(owner):
    ''' Function used for checking input '''
    in_file = '/tmp/piinput.json'
    
    while True:
        if os.path.exists(in_file):
            # Load file contents
            with open(in_file, 'r') as aFile:
                config = json.loads(aFile.readlines())
                owner.handle_input(config)
                
        time.sleep(1)
        
        
class Sensors(object):
    ''' Main class for the Sensors control '''

    def __init__(self):
        ''' Constructor '''
        self._cc2541  = cc2541.initialize_sensors()
        self._mcp3008 = mcp3008.initialize_sensors()
        self._lamp_and_pump = lampandpump.initialize_sensors()
        self._fan = fan.initialize_sensors()

        self._input_thread = InputThread()
        self._current_config = None

        
    def read_sensors(self):
        ''' Read all the sensors '''
        
        self._air_temp = self._cc2541.read_temperature()
        self._air_humidity = self._cc2541.read_humidity()
        self._ground_temp = self._cc2541.read_ground_temperature()
        self._door_open   = self._cc2541.read_door_status()

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

        self._lamp_and_pump.handle_light(self._light)
        self._lamp_and_pump.handle_pump(self._water_alarm, self._soil_humidity)

    def handle_input(self, config):
        ''' Handles input file '''

        # Available input values
        #  lamp         on/off/auto
        #  fan          on/off/auto
        #  airtemp_max  <val>    e.g "25.0" 

        if self._current_config == None:
            # All new config
            self._lamp_and_pump.handle_lamp_from_gui(config['lamp'])
            self._lamp_and_pump.handle_fan_from_gui(config['fan'])
            self._lamp_and_pump.set_airtemp_max(config['airtemp_max'])
        else:
            if config['lamp'] != self._current_config['lamp']:
                self._lamp_and_pump.handle_lamp_from_gui(config['lamp'])
            
#            if config['fan'] != self._current_config['fan']:
#                self._lamp_and_pump.handle_fan_from_gui(config['fan'])

#            if config['airtemp_max'] != self._current_config['airtemp_max']:
#                self._lamp_and_pump.set_airtemp_max(config['airtemp_max'])

        # Update current config
        self._current_config = config

    
    def main_loop(self):
        ''' Main program of the PiGreenHouse '''

        # Start input handling thread
        self._input_thread.start()

        
        # Enter main loop
        while True:
            time.sleep(5)
            
            sensors.read_sensors()
            sensors.analysis()
            sensors.store_sensors()
            
            sensors.check_input()
        
        

    
    
    

if __name__ == '__main__':
    print "Welcome to PiGreenHouse!"
    Sensors().main_loop()

    

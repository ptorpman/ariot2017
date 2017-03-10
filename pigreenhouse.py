#!/usr/bin/env python
#
# PiGreenHouse
#
# Authors: Altran Gnomes, (c) 2017
#
import time
import json
import os
import threading
import signal

from sensortag import cc2541
from sensortag import mcp3008
from sensortag import lampandpump
from sensortag import fan
from sensortag import camera

class InputThread(threading.Thread):
    ''' Threading class used for checking input '''
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)

def check_input_file(owner):
    ''' Function used for checking input '''
    in_file = './piinput.json'
    
    while True:
        if os.path.exists(in_file):
            # Load file contents
            with open(in_file, 'r') as aFile:
                contents = aFile.readlines()[0]
                print "CONTENTS: ", contents
                
                config = json.loads(contents)
                owner.handle_input(config)
        if owner.stop_input_thread:
            return
        time.sleep(1)
        
        
class Sensors(object):
    ''' Main class for the Sensors control '''

    def __init__(self):
        ''' Constructor '''
        self._cc2541  = cc2541.initialize_sensors()
        try:
            self._mcp3008 = mcp3008.initialize_sensors() 
        except Exception as exc:
            pass
        self._lamp_and_pump = lampandpump.initialize_sensors()
        self._fan = fan.initialize_sensors()
        self._camera = camera.initialize_sensors()

        self._input_thread = InputThread(check_input_file, self)
        self._current_config = None
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        
    def exit_gracefully(self, signum, frame):
        self.stop_input_thread = True
        print "* Exiting PiGreenHouse..."
        time.sleep(2)
        self._input_thread.join()


    def read_sensors(self):
        ''' Read all the sensors '''
        
        self._air_temp = self._cc2541.read_airtemperature()
        self._air_humidity = self._cc2541.read_humidity()
        self._ground_temp = self._cc2541.read_irtemperature()
        self._door_open   = self._cc2541.read_door_status()
        try:
            self._soil_humidity = self._mcp3008.read_soil_humidity()
            self._light = self._mcp3008.read_lightsensor()
            self._water_alarm = self._mcp3008.read_wateralarm()
        except Exception as exc:
            self._soil_humidity = 75.0
            self._light = 75.0
            self._water_alarm = False

    def store_sensors(self):
        ''' Store sensors to file '''
        to_store = {}

        to_store['AirTemp'] = self._air_temp
        to_store['AirHumidity'] = self._air_humidity
        to_store['GroundTemp'] = self._ground_temp
        to_store['SoilHumidity'] = self._soil_humidity
        to_store['Light'] = self._light
        to_store['WaterAlarm'] = self._water_alarm
        to_store['DoorOpen'] = self._door_open

        with open('./sensorvalues.json', 'w') as aFile:
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
        #  take_picture <timestamp>
        #  airtemp_max  <val>    e.g "25.0" 

        print "GOT INPUT: ", config
        
        if self._current_config == None:
            # All new config
            if config.has_key('lamp'):
                self._lamp_and_pump.handle_lamp_from_gui(config['lamp'])
            if config.has_key('fan'):
                self._fan.handle_fan_from_gui(config['fan'])
            if config.has_key('airtemp_max'):
                self._fan.set_airtemp_max(config['airtemp_max'])
            if config.has_key('take_picture'):
                self._camera.take_photo()
        else:
            if config.has_key('lamp') and \
               (config['lamp'] != self._current_config['lamp']):
                self._lamp_and_pump.handle_lamp_from_gui(config['lamp'])
            
            if config.has_key('fan') and \
               (config['fan'] != self._current_config['fan']):
                self._fan.handle_fan_from_gui(config['fan'])

            if config.has_key('airtemp_max') and \
               (config['airtemp_max'] != self._current_config['airtemp_max']):
                self._fan.set_airtemp_max(config['airtemp_max'])

            if config.has_key('take_picture') and \
               (config['take_picture'] != self._current_config['take_picture']):
                self._camera.take_photo()
                
        # Update current config
        self._current_config = config

    
    def main_loop(self):
        ''' Main program of the PiGreenHouse '''

        # Start input handling thread
        self.stop_input_thread = False
        self._input_thread.start()
        
        # Enter main loop
        while True:
            time.sleep(5)
            
            self.read_sensors()
            self.analysis()
            self.store_sensors()
        
        

    
    
    

if __name__ == '__main__':
    print "Welcome to PiGreenHouse!"
    Sensors().main_loop()

    

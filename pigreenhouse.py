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
import socket
import subprocess

from sensortag import cc2541
from sensortag import mcp3008
from sensortag import lampandpump
from sensortag import fan
from sensortag import camera
from sensortag import sensorutils

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
                try:
                    contents = aFile.readlines()[0]
                    config = json.loads(contents)
                    owner.handle_input(config)
                except Exception as exc:
                    print "* Input file problems..."
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

        self._average = {}
        self._average['airtemp'] = 0.0
        self._average['airhumidity'] = 0.0
        self._average['groundtemp'] = 0.0
        self._average['light'] = 0.0
        self._average['soilhumidity'] = 0.0

        self._sum_readings = {}
        self._sum_readings['airtemp'] = 0.0
        self._sum_readings['airhumidity'] = 0.0
        self._sum_readings['groundtemp'] = 0.0
        self._sum_readings['light'] = 0.0
        self._sum_readings['soilhumidity'] = 0.0
        
        self._average_num_measurements = 0
        
        
    def exit_gracefully(self, signum, frame):
        self.stop_input_thread = True
        print "* Exiting PiGreenHouse..."
        time.sleep(2)
        self._input_thread.join()

        try:
            os.remove('./piinput.json')
        except Exception as exc:
            pass


    def read_sensors(self):
        ''' Read all the sensors '''
        
        self._air_temp = self._cc2541.read_airtemperature()
        self._air_humidity = self._cc2541.read_humidity()
        self._ground_temp = self._cc2541.read_irtemperature()
        self._door_open   = self._cc2541.read_door_status()
        self._soil_humidity = self._mcp3008.read_soil_humidity()
        self._light = self._mcp3008.read_lightsensor()
        self._water_alarm = self._mcp3008.read_water_status()

        self._sum_readings['airtemp'] += self._air_temp
        self._sum_readings['airhumidity'] += self._air_humidity
        self._sum_readings['groundtemp'] += self._ground_temp
        self._sum_readings['light'] += self._light
        self._sum_readings['soilhumidity'] += self._soil_humidity

        self._average_num_measurements += 1

        self._average['airtemp'] = self._sum_readings['airtemp']  / self._average_num_measurements
        self._average['airhumidity'] = self._sum_readings['airhumidity'] / self._average_num_measurements
        self._average['groundtemp'] = self._sum_readings['groundtemp'] / self._average_num_measurements
        self._average['light'] = self._sum_readings['light'] / self._average_num_measurements
        self._average['soilhumidity'] = self._sum_readings['soilhumidity'] / self._average_num_measurements

        
    def store_sensors(self):
        ''' Store sensors to file '''
        to_store = {}

        to_store['AirTemp'] = [self._air_temp, self._average['airtemp']]
        to_store['AirHumidity'] = [self._air_humidity, self._average['airhumidity']]
        to_store['GroundTemp'] = [self._ground_temp, self._average['groundtemp']]
        to_store['SoilHumidity'] = [self._soil_humidity, self._average['soilhumidity']]
        to_store['Light'] = [self._light, self._average['light']]
        to_store['WaterAlarm'] = self._water_alarm
        to_store['DoorOpen'] = self._door_open
        to_store['FanIsOn'] = self._fan.get_fan_on()
        to_store['PumpIsOn'] = self._lamp_and_pump.get_pump_on()
        to_store['LampIsOn'] = self._lamp_and_pump.get_lamp_on()
        
        with open('./sensorvalues.json', 'w') as aFile:
            aFile.write(json.dumps(to_store))

        print "* Stored values to /tmp/sensorvalues.json"
            
    def analysis(self):
        ''' Perform some analysis based on the sensor values '''

        self._lamp_and_pump.handle_light(self._light)
        self._lamp_and_pump.handle_pump(self._water_alarm, self._soil_humidity)
        self._fan.handle_fan(self._air_temp)

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
                print "UPDATING LAMP"
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

        self.publish_ip()
        
        # Start input handling thread
        self.stop_input_thread = False
        self._input_thread.start()
        
        # Enter main loop
        while True:
            time.sleep(1)
            self.read_sensors()
            self.analysis()
            self.store_sensors()
        
        
    def publish_ip(self):
        ''' Store public IP address to Dropbox '''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))

        ip = s.getsockname()[0]

        with open('./ip.txt', 'w') as aFile:
            aFile.write(ip)

        sensorutils.upload_to_cloud('./ip.txt')
            
            

if __name__ == '__main__':
    print "Welcome to PiGreenHouse!"
    Sensors().main_loop()

    

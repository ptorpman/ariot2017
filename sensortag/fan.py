# This file is part of PiGreenHouse
# Author: Altran Gnomes, 2017
#
import RPi.GPIO as GPIO
import time

class Fan(object):
    ''' This class handles the fan '''
    def __init__(self):
        ''' Constructor '''
        self._max_air_temp = 20.0
        self._manual_mode = False

        # setup output pins
        GPIO.setmode(GPIO.BOARD) 
        GPIO.setup(8,GPIO.OUT)
        GPIO.setup(10,GPIO.OUT)
        GPIO.setup(12,GPIO.OUT)
        GPIO.output(8,GPIO.LOW)
        GPIO.output(10,GPIO.HIGH)

    def handle_fan_from_gui(self, value):
        ''' Change fan from GUI '''

        if value == 'on':
            self.turn_on_fan()
            self._manual_mode = True
        elif value == 'off':
            self.turn_off_fan()
            self._manual_mode = True
        else:
            # Auto
            self._manual_mode = False

    def set_airtemp_max(self, value):
        ''' Set max air temp value '''
        self._max_air_temp = float(value)
    
    def handle_fan(self, air_temp):
        ''' Handle fan depending on air temperature '''
        if air_temp > self._max_air_temp:
            self.turn_on_fan() 
        else:
            self.turn_off_fan() 

    def turn_on_fan(self):
        ''' Turns on the fan '''
        GPIO.output(12,GPIO.HIGH)


    def turn_off_fan(self):
        ''' Turns off the fan '''
        GPIO.output(12,GPIO.LOW)


    
# LIBRARY FUNCTIONS

def initialize_sensors():
    return Fan()


if __name__ == '__main__':
    f = initialize_sensors()

    f.turn_on_fan()
    time.sleep(2)
    f.turn_off_fan()
    
    

        

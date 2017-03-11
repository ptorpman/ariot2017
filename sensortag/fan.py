# This file is part of PiGreenHouse
# Author: Altran Gnomes, 2017
#
import RPi.GPIO as GPIO
import time

class Fan(object):
    ''' This class handles the fan '''
    def __init__(self):
        ''' Constructor '''
        self._max_air_temp = 22.05
        self._manual_mode = False
        self._fan_on = False

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
            return
        
        if value == 'off':
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

        print "HANDLE FAN. TEMP: ", air_temp
        print "HANDLE FAN. MAX: ", self._max_air_temp
        
        if float(air_temp) > self._max_air_temp:
            print "* Turning on fan to cool stuff down..."
            self.turn_on_fan() 
        else:
            print "* Turning off the fan."
            self.turn_off_fan() 

    def turn_on_fan(self):
        ''' Turns on the fan '''
        GPIO.output(12,GPIO.HIGH)
        self._fan_on = True


    def turn_off_fan(self):
        ''' Turns off the fan '''
        GPIO.output(12,GPIO.LOW)
        self._fan_on = False

    def get_fan_on(self):
        ''' Return if fan is on or off '''
        return self._fan_on
    
# LIBRARY FUNCTIONS

def initialize_sensors():
    return Fan()


if __name__ == '__main__':
    f = initialize_sensors()

    f.turn_on_fan()
    time.sleep(2)
    f.turn_off_fan()
    
    

        

# This file is part of PiGreenHouse
# Author: Altran Gnomes, 2017
#

class Fan(object):
    ''' This class handles the fan '''
    def __init__(self):
        ''' Constructor '''
        self._max_air_temp = 20.0
        self._manual_mode = False

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
        pass

    def turn_off_fan(self):
        ''' Turns on the fan '''
        pass
    
# LIBRARY FUNCTIONS

def initialize_sensors():
    return Fan()

# This file is part of PiGreenHouse
# Author: Altran Gnomes, 2017
#
import RPi.GPIO as GPIO
import datetime

class LampAndPump(object):

    def __init__(self, lamp_port, pump_port):
        ''' Constructor '''
        self._lamp_port = lamp_port
        self._pump_port = pump_port
        
        GPIO.setmode(GPIO.BOARD) 
        GPIO.setup(self._lamp_port, GPIO.OUT)
        GPIO.setup(self._pump_port, GPIO.OUT) 
        GPIO.output(self._lamp_port, GPIO.LOW)
        GPIO.output(self._pump_port, GPIO.LOW)

        self._lamp_on = False
        self._pump_on = False

    def lamp_on(self):
        ''' Turn lamp on '''
        GPIO.output(self._lamp_port,GPIO.HIGH)
        self._lamp_on = True

    def lamp_off(self):
        ''' Turn lamp off '''
        GPIO.output(self._lamp_port,GPIO.LOW)
        self._lamp_on = False

    def pump_on(self):
        ''' Turn pump on '''
        GPIO.output(self._pump_port,GPIO.HIGH)
        self._pump_on = True

    def pump_off(self):
        ''' Turn lamp off '''
        GPIO.output(self._pump_port,GPIO.LOW)
        self._pump_on = False

    def handle_light(self, light_value):
        ''' Turn the lamp on depending on light value and time of day '''

        now = datetime.datetime.now()

        # Light should be on on in the interval 0900 to 2100

        if now.hour >= 9 and now.hour < 21:
            # Within the interval
            if light_value < 50.0:
                self.lamp_on()
        else:
            # Outside, make sure lamp is off
            self.lamp_off()
        
        

# LIBRARY FUNCTIONS

def initialize_sensors():
    lp = LampAndPump(lamp_port=36, pump_port=38)
    return lp



# This file is part of PiGreenHouse
# Author: Altran Gnomes, 2017
#
import RPi.GPIO as GPIO

class LampAndPump(object):
  def __init__(self, lamp_port, pump_port):
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(lamp_port,GPIO.OUT)
    GPIO.setup(pump_port,GPIO.OUT) 
    GPIO.output(lamp_port,GPIO.LOW)
    GPIO.output(pump_port,GPIO.LOW)


def lamp(on):
  if on:
    GPIO.output(lamp_port,GPIO.HIGH)
  else:
    GPIO.output(lamp_port,GPIO.LOW)
    
def pump(on):
  if on:
    GPIO.output(pump_port,GPIO.HIGH)
  else:
    GPIO.output(pump_port,GPIO.LOW)
    

# LIBRARY FUNCTIONS

def initialize_sensors():
    lp = LampAndPump(lamp_port=36, pump_port=38)
    return lp



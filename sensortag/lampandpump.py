# This file is part of PiGreenHouse
# Author: Altran Gnomes, 2017
#
import RPi.GPIO as GPIO
import datetime
import time
import threading
import sys

class PumpRunner(threading.Thread):
    ''' Threading class used for running the pump '''
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)

def run_the_pump(owner):
    ''' Thread method to run the pump for a while '''
    print "* Turning pump on..."
    owner.pump_on()
    print "* Waiting 10 seconds..."
    time.sleep(10)
    print "* Turning pump off..."
    owner.pump_off()
    owner.pump_thread_done = True
    

class LampAndPump(object):
    ''' Class used for handling lamp and pump '''

    def __init__(self, lamp_port, pump_port):
        ''' Constructor '''
        self._lamp_port = lamp_port
        self._pump_port = pump_port

        self.pump_thread_done = False
        self._pump_thread = None

        self._backoff_time = 120
        
        GPIO.setmode(GPIO.BOARD) 
        GPIO.setup(self._lamp_port, GPIO.OUT)
        GPIO.setup(self._pump_port, GPIO.OUT) 
        GPIO.output(self._lamp_port, GPIO.LOW)
        GPIO.output(self._pump_port, GPIO.LOW)

        self._lamp_on = False
        self._lamp_manual_mode = False

        self._pump_on = False
        self._pump_started = None

    def lamp_on(self):
        ''' Turn lamp on '''
        print "* Turn lamp ON"
        GPIO.output(self._lamp_port,GPIO.HIGH)
        self._lamp_on = True

    def lamp_off(self):
        ''' Turn lamp off '''
        print "* Turn lamp OFF"
        GPIO.output(self._lamp_port,GPIO.LOW)
        self._lamp_on = False

    def pump_on(self):
        ''' Turn pump on '''
        GPIO.output(self._pump_port,GPIO.HIGH)
        self._pump_on = True
        self._pump_started = int(time.time())

    def pump_off(self):
        ''' Turn lamp off '''
        GPIO.output(self._pump_port,GPIO.LOW)
        self._pump_on = False

    def handle_light(self, light_value):
        ''' Turn the lamp on depending on light value and time of day '''

        now = datetime.datetime.now()

        # Light should be on on in the interval 0900 to 2100

        if self._lamp_manual_mode:
            return
        
        if now.hour >= 9 and now.hour < 21:
            print "* Within light interval", float(light_value)
            # Within the interval
            
            if float(light_value) < 50.0:
                self.lamp_on()
            else:
                self.lamp_off()
        else:
            # Outside, make sure lamp is off
            self.lamp_off()

    def allowed_to_run_pump(self):
        ''' Safe guard that we do not run the pump too often '''

        # Make sure we do not run the pump too often
        if self._pump_started == None:
            # Pump never started
            return True

        if self._pump_on:
            # Pump already running
            return False
            
        if (int(time.time()) - self._pump_started) < self._backoff_time:
            print "* Pump not started. Next possible start in %d seconds" % (self._backoff_time - (int(time.time()) - self._pump_started))
            return False

        return True

        
    def handle_pump(self, alarm_value, soil_humidity):
        ''' Handle the pump based on the water alarm '''

        # If pump thread has been started, see if we can join it
        if self._pump_thread != None:
            if self.pump_thread_done:
                self._pump_thread.join()
                self._pump_thread = None
                self.pump_thread_done = False

        print "* Water Level is : ", alarm_value
                
        if alarm_value == "red":           
            self.pump_off()
            return

        # If humidity is too low we need to run the pump for a while
        if float(soil_humidity) <  25.0:
            self.run_the_pump()

    def run_the_pump(self):
        ''' Run the pump '''

        if not self.allowed_to_run_pump():
            print "* Not allowed to run the pump yet"
            return
        
        self.pump_thread_done = False
        self._pump_thread = PumpRunner(run_the_pump, self)
        self._pump_thread.start()
        

    def handle_lamp_from_gui(self, value):
        ''' Change lamp from GUI '''

        if value == 'on':
            self.lamp_on()
            self._lamp_manual_mode = True
            return
        
        if value == 'off':
            self.lamp_off()
            self._lamp_manual_mode = True
        else:
            # Auto
            self._lamp_manual_mode = False

    def get_lamp_on(self):
        ''' Return if the lamp is on or off '''
        return self._lamp_on
    
    def get_pump_on(self):
        ''' Return if the pump is on or off '''
        return self._pump_on

# LIBRARY FUNCTIONS

def initialize_sensors():
    return LampAndPump(lamp_port=36, pump_port=38)


if __name__ == '__main__':

    l = initialize_sensors()

    print "RUNNING PUMP: ", sys.argv[1]

    if sys.argv[1] == "1":
        l.lamp_on()
        l.pump_on()
        
    if sys.argv[1] == "0":
        l.pump_off()
        l.lamp_off()
    

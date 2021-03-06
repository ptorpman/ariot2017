#!/usr/bin/env python
# Code to read the sensors and control the environment for the the best conditions to our greenhouse plants.


import time
import sys
#sys.path.append('/usr/local/lib/python2.7/dist-packages/bluepy')
from bluepy import btle
from bluepy import sensortag



class TempAndHumidity(object):
	def __init__(self, mac='BC:6A:29:AC:53:91'):
		''' Constructor '''
		print "* Connecting to sensor..."
		self._tag = sensortag.SensorTag(addr=mac)
		print "* Connected: ", self._tag
		self._tag.magnetometer.enable()
		self._tag.IRtemperature.enable()
		self._tag.humidity.enable()
		self._tag.IRtemperature.enable()
		self._tag.barometer.enable()
		self._tag.accelerometer.enable()
		self._tag.gyroscope.enable()
		time.sleep(2.0)
		print "* Sensors enabled"
	
		self._temp_value = 0.0

	def read_irtemperature(self):		
		self._temp_value = self._tag.IRtemperature.read()
		return self._temp_value[1]
	
	def read_humidity(self):
		self._hum_value = self._tag.humidity.read()		
		return self._hum_value[1]
	
	def read_airtemperature(self):
		self._temp_value = self._tag.IRtemperature.read()
		return self._temp_value[0]
	
	def read_barometer(self):
		self._baro_value = self._tag.barometer.read()
		return self._baro_value[1]
		
	def read_accelerometer(self):
		self._acce_value = self._tag.accelerometer.read()
		return self._acce_value
		
	def read_gyroscope(self):	
		self._gero_value = self._tag.gyroscope.read()
		return self._gero_value
		
	def read_magnetometer(self):
		self._magn_value = self._tag.magnetometer.read()
		return self._magn_value
	
	def read_door_status(self):
		z_axis=self.read_magnetometer()[2]
		#door_status=0 means door is closed
		#dorr_status=1 means door is open
		if z_axis >-46:
			door_status = True
		else:
			door_status = False
		return door_status
	
	#def read_moving_status(self, gero_value):
	#	
	#	if gero_value[0]<-2:
			
		
	

def initialize_sensors():
    return TempAndHumidity()

#mac = 'BC:6A:29:AC:53:91'

# Instantiate..


def main():
	print "IRtemp is " , tah.read_irtemperature()
	print "Airtemp is " , tah.read_airtemperature()
	print "Humidity is ", tah.read_humidity()
	print "preasure is ", tah.read_barometer()
	print "accelerometer is ", tah.read_accelerometer()
	print "coordinates are ", tah.read_gyroscope()
	print "magnetometer is  ", tah.read_magnetometer()
	print "door_status is ", tah.read_door_status()


if __name__ == '__main__':
    print "Welcome to PiGreenHouse!"
    tah = TempAndHumidity()
    main()




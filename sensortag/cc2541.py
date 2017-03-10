#!/usr/bin/env python
# Code to read the sensors and control the environment for the the best conditions to our greenhouse plants.


import time
import sys
#sys.path.append('/usr/local/lib/python2.7/dist-packages/bluepy')
from bluepy import btle
from bluepy import sensortag

class TempAndHumidity(object):
	def __init__(self, mac):
		''' Constructor '''
		print "* Connecting to sensor..."
		self._tag = sensortag.SensorTag(addr=mac)
		print "* Connected: ", self._tag
		
	
		self._temp_value = 0.0

	def read_irtemperature(self):
		self._tag.IRtemperature.enable()
		time.sleep(1.0)
		self._temp_value = self._tag.IRtemperature.read()

		return self._temp_value[1]
	
	def read_humidity(self):
		self._tag.humidity.enable()
		time.sleep(1.0)
		self._hum_value = self._tag.humidity.read()
		
		return self._hum_value[1]
	
	def read_airtemperature(self):
		self._tag.IRtemperature.enable()
		time.sleep(1.0)
		self._temp_value = self._tag.IRtemperature.read()

		return self._temp_value[0]


		
		

def read_sensor_values(tag):
	#if sensor==1:
	#read IRTemp
	tag.IRtemperature.enable()
	value=tag.IRtemperature.read()
	print value
	return value
	#lif sensor==2:
	#	#read AmbTemp
	#	value = sensortag(mac, '-T', '-n 1')
	#	return value[1][1]
	#elif sensor==3:
	#	#read Humidity
	#	value = sensortag(mac, '-H', '-n 1')
	#	return value[1][1]
	#else:
	#	#error "given value not reqognized"
	#	print "error value not recognized"
	#return

#print "Instantiating..."
#tag = 
#read_sensor_values(tag)

mac = 'BC:6A:29:AC:53:91'

# Instantiate..
tah = TempAndHumidity(mac)

print "IRtemp is " , tah.read_irtemperature()
print "Airtemp is " , tah.read_airtemperature()
print "Humidity is ", tah.read_humidity()



# Sensortag

# Air temperature sensor reading


# Control of the air temperature (turning the fan on and off)



# Ground temperature sensor reading
# NO CONTROL!!



# Air humidity sensor reading
# NO CONTROL!!









# Light sensor reading 
# Control of the light (turning the pump on and off)

# WHEN??



# Ground humidity sensor reading
# Control of the ground humidity (turning the water on and off)



# Water level in the can reading

# TOP OR BOTTOM??



# Camera capture in the mobile app!











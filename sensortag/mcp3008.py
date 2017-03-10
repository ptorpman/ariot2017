# This file is part of PiGreenHouse
# Author: Altran Gnomes, 2017
#
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

class Mcp3008(object):

    def __init__(self, device, port):
        ''' Constructor '''
        print "* Initializing MCP3008..."
        self._mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(port, device))
        print "* Initializing MCP3008... done!"

    def read_soil_humidity(self):
        ''' Returns soil humidity in percent '''
        value = self._mcp.read_adc(7)
        # 1023 means totally dry, 0 means completely wet
        return ((1023-value)*100 / 1023)
     
    def read_lightsensor(self):
        ''' Returns light value in percent '''
        # 1023 means totally light, 0 means completely night
        value = self._mcp.read_adc(0)
        return (value * 100/ 1023)
    
    def read_wateralarm(self):
        ''' Returns if water alarm is on or off '''
        value = self._mcp.read_adc(5)

        if value > 1000:
            return True
        else:
            return False

        
# LIBRARY FUNCTIONS

def initialize_sensors():
    mcp = Mcp3008(device=0, port=0)
    return mcp


if __name__ == '__main__':

    mcp = initialize_sensors()

    print mcp.read_soil_humidity();
    print mcp.read_lightsensor();
    print mcp.read_wateralarm();
    

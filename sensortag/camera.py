# This file is part of PiGreenHouse
# Author: Altran Gnomes, 2017
#

from picamera import PiCamera
from time import sleep
import time


class Camera(object):
    ''' Class for handling the camera '''
    def __init__(self):
        ''' Constructor '''
        self._cam = PiCamera()
        self._cam.resolution = (800, 600)

        # Camera warmup time
        time.sleep(2)

    def take_photo(self):
        ''' Take a picture '''
        try:
            img = 'image' + str(int(round(time.time() * 1000))) + '.jpg'
            self._cam.capture('./static/photos/' + img)
        finally:
            return 'Hello world!'

# LIBRARY FUNCTIONS
        
def initialize_sensors():
    return Camera()


    

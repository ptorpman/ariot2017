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

        # Camera warmup time
        time.sleep(2)

    def take_photo(self):

        try:
            img = 'image' + str(int(round(time.time() * 1000))) + '.jpg'
            camera.capture('./static/images/' + img)
        finally:
            camera.close()
            return 'Hello world!'


# LIBRARY FUNCTIONS
        
def initialize_sensors():
    return Camera()


    

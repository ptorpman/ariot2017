# This file is part of PiGreenHouse
# Author: Altran Gnomes, 2017
#

from picamera import PiCamera
from time import sleep
import time
import os
from sensortag import sensorutils


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

        img = 'image' + str(int(round(time.time() * 1000))) + '.jpg'

        img_path = './static/photos/%s' % img
        
        try:
            self._cam.capture(img_path)
        finally:
            pass

        sensorutils.upload_to_cloud(img_path)

        
# LIBRARY FUNCTIONS
        
def initialize_sensors():
    return Camera()


    

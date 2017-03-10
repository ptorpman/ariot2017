# This file is part of PiGreenHouse
# Author: Altran Gnomes, 2017
#

from picamera import PiCamera
from time import sleep
import time
import subprocess
import os

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

        self.upload_to_cloud(img_path)

    def upload_to_cloud(self, img_path):
        ''' Upload to dropbox '''

        img_file = os.path.basename(img_path)
        
        cmd = "./dropbox_uploader.sh upload %s %s" % (img_path, img_file)
        
        try:
            subprocess.call([cmd], shell=True)
            print "* Photo uploaded to dropbox"
        except Exception as exc:

            pass

        
# LIBRARY FUNCTIONS
        
def initialize_sensors():
    return Camera()


    

from picamera import PiCamera
from time import sleep
import time




def altranCapture():
    
    camera = PiCamera()
    try:
        img = 'image' + str(int(round(time.time() * 1000))) + '.jpg'
        sleep(5)
        camera.capture('/home/pi/Desktop/' + img)
    finally:
        camera.close()
        return 'Hello world!'


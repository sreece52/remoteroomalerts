import RPi.GPIO as GPIO
from gpiozero import MotionSensor
import datetime
import time
from time import sleep
import piCameraModule
from piCameraModule import Camera

class motionSensor:
   
   pir = MotionSensor(25) # setup pin 25 as input for the motion sensor
   
   def __init__(self):
      # configure the GPIO pin mode    
      self.camera = Camera()
      self.camera.__init__()
           
   def detectMotion(self):
      while(1):
         #loop that keeps polling the pins
         if motionSensor.pir.motion_detected: # if the pins status changes we enter this if
            localTime = '{:%H:%M:%S}'.format(datetime.datetime.now())
            print("Motion detected at " + localTime) # prints notification
            self.camera.takePicture()
            time.sleep(10) # wait for ten secs
         else: # if state unchanged we enteclar this condition
            print("No Motion detected") # simple print
            time.sleep(1) # sleep for one sec

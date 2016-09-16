from gpiozero import MotionSensor
from time import gmtime, strftime
import RPi.GPIO as GPIO
import time

#---------------------------------------------------------------------------#
# see raspberry pi pin layout to connect to a pin
# wiring sensor: VCC connect to any 5v pin
#                GND connect to any grounded location on broad or else where
#                OUT connect to pin 4
#---------------------------------------------------------------------------#

# note: led is not important for the sensor and other code to run
# just comment out the code regarding the led if you dont need it.
# Was using it during testing.

pir = MotionSensor(4) # configures pin 4 as the inout for the sensor
GPIO.setmode(GPIO.BCM) # settings for the led
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

#loop that keeps polling the pins
while(1):
    GPIO.output(18,GPIO.LOW) # make sure the led is off
    if pir.motion_detected: # if the pins status changes we enter this if
        localTime = time.localtime(time.time()) # gets local time stamp
        print("Motion detected " , localTime) # prints notification
        GPIO.output(18,GPIO.HIGH) # turns on led.
        time.sleep(10) # wait for ten secs


    else: # if state unchanged we enter this condition
        print("No Motion detected") # simple print
        GPIO.output(18,GPIO.LOW) # turn off the led.
        time.sleep(1) # sleep for one sec

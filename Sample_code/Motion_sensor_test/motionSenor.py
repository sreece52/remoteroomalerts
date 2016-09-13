from gpiozero import MotionSensor
from time import gmtime, strftime
import RPi.GPIO as GPIO
import time

pir = MotionSensor(4)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

while(1):
    GPIO.output(18,GPIO.LOW)
    if pir.motion_detected:
        localTime = time.localtime(time.time())
        print("Motion detected " , localTime)
        GPIO.output(18,GPIO.HIGH)
        time.sleep(10)
        

    else:
        print("No Motion detected")
        GPIO.output(18,GPIO.LOW)
        time.sleep(1)

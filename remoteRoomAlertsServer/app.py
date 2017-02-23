#!/usr/bin/env python
import RPi.GPIO as GPIO
from flask import Flask, render_template, Response, request
from gpiozero import MotionSensor
import os
from time import gmtime, strftime, sleep
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from picamera import PiCamera
import threading

# root path for files
app = Flask(__name__)

# configure the GPIO pin mode
GPIO.setmode(GPIO.BCM)

# configure pins for servos
GPIO.setup(18, GPIO.OUT)
pwmHorizontal = GPIO.PWM(18, 100)
pwmHorizontal.start(5)
GPIO.setup(23, GPIO.OUT)
pwmVertical = GPIO.PWM(23, 100)
pwmVertical.start(5)

# setting up the camera
camera = PiCamera()
camera.rotation = 180

pir = MotionSensor(25) # configures gpio pin 25 as the inout for the sensor
isMotionDetected = False

# Establish a secure session with Gmail's
# outgoing SMTP server using your gmail account
#server = smtplib.SMTP("smtp.gmail.com", 587)

# Puts the SMTP connection in TLS (Transport Layer Security Mode
# All SMTP commands that follow will be encrypted
#server.starttls()

# Parameters: login using your Gmail address and password
#server.login()

# Sender and receiver for email
sender = "Pi"
receiver = ""

# where to save picture to
image_path = '/home/pi/github/remoteroomalerts/remoteRoomAlertsServer/static/image.jpg'

# Set servos to starting position
horizontalPosition = 11.5
verticalPosition = 11.5
pwmHorizontal.ChangeDutyCycle(horizontalPosition)
pwmVertical.ChangeDutyCycle(verticalPosition)

def takePicture():
   global isMotionDetected
   
   camera.capture(image_path)
   
   if (isMotionDetected == True):
      #sendEmail()
      isMotionDetected = False

# Message creation
# This message format must be used because message headers must be included
# A subject header can also be used after the To header
def sendEmail():
    img_data = open(image_path, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Security Alert'
    msg['From'] = sender
    msg['To'] = receiver
    text = MIMEText('Motion has been detected!')
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(image_path))
    msg.attach(image)
    server.sendmail(sender, receiver, msg.as_string())
    
def detectMotion():
   global isMotionDetected
   
   while(1):
      #loop that keeps polling the pins
      if pir.motion_detected: # if the pins status changes we enter this if
         isMotionDetected = True
         localTime = time.localtime(time.time()) # gets local time stamp
         print("Motion detected " , localTime) # prints notification
         takePicture()
         time.sleep(10) # wait for ten secs
      else: # if state unchanged we enter this condition
         isMotionDetected = False
         print("No Motion detected") # simple print
         time.sleep(1) # sleep for one sec

def moveServo(direction):
   global horizontalPosition
   global verticalPosition
   
   if (direction == "Left"):
      if (horizontalPosition < 20.5):
         horizontalPosition += 1
         pwmHorizontal.ChangeDutyCycle(horizontalPosition)
   elif (direction == "Right"):
      if (horizontalPosition > 2.5):
         horizontalPosition -= 1
         pwmHorizontal.ChangeDutyCycle(horizontalPosition)
   elif (direction == "Up"):
      if (verticalPosition > 2.5):
         verticalPosition -= 1
         pwmVertical.ChangeDutyCycle(verticalPosition)
   elif (direction == "Down"):
      if (verticalPosition < 20.5):
         verticalPosition += 1
         pwmVertical.ChangeDutyCycle(verticalPosition)

@app.after_request
def add_header(response):
   response.headers['Cache-Control'] = 'public, max-age=0'
   return response

#root directory
# get and post allows us to rebuild the site when an action occurs
@app.route('/', methods=['GET','POST'])
def index():   
   """Video streaming home page."""
   if request.method == "GET":
      return render_template('index.html')
   else:
      moveServo(request.form.get("button", None))
      takePicture()
      return render_template('index.html')
   
if __name__ == '__main__':
   motionThread = threading.Thread(target = detectMotion)
   motionThread.start()
   app.config['TEMPLATES_AUTO_RELOAD'] = True
   app.run()

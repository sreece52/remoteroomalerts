#!/usr/bin/env python
import RPi.GPIO as GPIO
from flask import Flask, render_template, Response, request, jsonify
from gpiozero import MotionSensor
import os
from time import gmtime, strftime, sleep
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import Adafruit_PCA9685
from picamera import PiCamera
import threading

# configure the GPIO pin mode
GPIO.setmode(GPIO.BCM)

pir = MotionSensor(25) # configures gpio pin 25 as the inout for the sensor
isMotionDetected = False

# Set servos to starting position
horizontalPosition = 350
verticalPosition = 350

# setting up the servos
pwm = Adafruit_PCA9685.PCA9685()
servo_min = 150
servo_max = 600
pwm.set_pwm_freq(60)
pwm.set_pwm(0,0,horizontalPosition)
pwm.set_pwm(1,0,verticalPosition)

# setting up the camera
camera = PiCamera()
camera.rotation = 180

# Establish a secure session with Gmail's
# outgoing SMTP server using your gmail account
server = smtplib.SMTP("smtp.gmail.com", 587)

# Puts the SMTP connection in TLS (Transport Layer Security Mode
# All SMTP commands that follow will be encrypted
server.starttls()

# Parameters: login using your Gmail address and password
server.login()

# Sender and receiver for email
sender = "Pi"
receiver = "" #add email here

# where to save picture to
image_path = '/home/pi/github/remoteroomalerts/remoteRoomAlertsServer/static/photos/image.jpg'

def takePicture():
   global isMotionDetected
   
   camera.capture(image_path)
   
   if (isMotionDetected == True):
      sendEmail()
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
   servo_min = 150
   servo_max = 600
   increment = 10
  
   if (direction == "L"):
      if (horizontalPosition < servo_max):
         horizontalPosition += increment
         pwm.set_pwm(0,0,horizontalPosition)
   elif (direction == "R"):
      if (horizontalPosition > servo_min):
         horizontalPosition -= increment
         pwm.set_pwm(0,0,horizontalPosition)
   elif (direction == "U"):
      if (verticalPosition > servo_min):
         verticalPosition -= increment
         pwm.set_pwm(1,0,verticalPosition)
   elif (direction == "D"):
      if (verticalPosition < servo_max):
         verticalPosition += increment
         pwm.set_pwm(1,0,verticalPosition)

# root path for files
app = Flask(__name__)

@app.after_request
def add_header(response):
   response.headers['Cache-Control'] = 'public, max-age=0'
   return response

@app.route('/keydown', methods = ['POST'])
def buttonHandle():
   direction = request.json[0]
   direction = str(direction)
   direction.strip()
   moveServo(direction)
   return jsonify(result = 0)

#root directory
# get and post allows us to rebuild the site when an action occurs
@app.route('/', methods = ['GET'])
def index():   
   """Video streaming home page."""
   return render_template('index.html')

if __name__ == '__main__':
   motionThread = threading.Thread(target = detectMotion)
   motionThread.daemon = True # allows thread to  exit when main thread exits
   motionThread.start()    
      
   app.config['TEMPLATES_AUTO_RELOAD'] = True   
   #app.run() #add ip and port here to access stream over internet
   app.run(host='192.168.0.103', port=5000) # local connection
   

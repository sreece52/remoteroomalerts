#!/usr/bin/env python
import RPi.GPIO as GPIO
from flask import Flask, render_template, Response, request

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera

#root path for files
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwmHorizontal = GPIO.PWM(18, 100)
pwmHorizontal.start(5)

GPIO.setup(23, GPIO.OUT)
pwmVertical = GPIO.PWM(23, 100)
pwmVertical.start(5)

horizontalPosition = 11.5
verticalPosition = 11.5

pwmHorizontal.ChangeDutyCycle(horizontalPosition)
pwmVertical.ChangeDutyCycle(verticalPosition)

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
   
def gen(camera):
   """Video streaming generator function."""
   while True:
      frame = camera.get_frame()
      yield (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#root directory
# get and post allows us to rebuild the site when an action occurs
@app.route('/', methods=['GET','POST'])
def index():
   """Video streaming home page."""
   if request.method == "GET":
      return render_template('index.html')
   else:
      moveServo(request.form.get("button", None))
      return render_template('index.html')


@app.route('/video_feed')
def video_feed():
   return Response(gen(Camera()),
                   mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run()

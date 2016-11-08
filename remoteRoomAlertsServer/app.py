#!/usr/bin/env python
import RPi.GPIO as GPIO
from flask import Flask, render_template, Response, request

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera

#root path for files
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pin = {'PinNum': '18', 'pinName' : 'GPIO 18', 'state' : GPIO.LOW}

# Set each pin as an output and make it low:
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)

#root directory
# get and post allows us to rebuild the site when an action occurs
@app.route('/', methods=['GET','POST'])
def index():
   """Video streaming home page."""
   if request.method == "GET":
      return render_template('index.html')
   else:
      test()
      return render_template('index.html')


def gen(camera):
   """Video streaming generator function."""
   while True:
      frame = camera.get_frame()
      yield (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

      
def test():
   print("button pressed")

 
@app.route('/video_feed')
def video_feed():
   return Response(gen(Camera()),
                   mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run()

#!/usr/bin/env python
from flask import Flask, render_template, Response, request, jsonify
import threading
from modules.motionSensorModule import motionSensor
from modules.servosModule import Servos
import RPi.GPIO as GPIO

servos = Servos() # servos object
servos.__init__() # initializes the servos

# root path for files
app = Flask(__name__)

@app.after_request
def add_header(response):
   response.headers['Cache-Control'] = 'public, max-age=0'
   return response

# handles POST request from the webpage
@app.route('/keydown', methods = ['POST'])
def buttonHandle():
   direction = request.json[0]
   direction = str(direction)
   direction.strip()
   servos.moveServo(direction)
   return jsonify(result = 0)

#root directory
# handles GET requests
@app.route('/', methods = ['GET'])
def index():   
   """Video streaming home page."""
   return render_template('index.html')

# starts the motion thread and starts the server
if __name__ == '__main__':
   sensor = motionSensor()
   motionThread = threading.Thread(target = sensor.detectMotion)
   motionThread.daemon = True # allows thread to  exit when main thread exits
   motionThread.start()

   print("Starting server...")
   app.config['TEMPLATES_AUTO_RELOAD'] = True   
   app.run(host = 'add ip address here', port='add port number here no quotes') #add ip and port here to access stream over internet
   #app.run(host='192.168.0.1', port=5000) # local connection dont use this is an example
   

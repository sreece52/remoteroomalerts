from gpiozero import MotionSensor
import os
from time import gmtime, strftime, sleep
from picamera import PiCamera
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

camera = PiCamera()
camera.rotation = 180
pir = MotionSensor(4) # configures pin 4 as the inout for the sensor

# Establish a secure session with Gmail's
# outgoing SMTP server using your gmail account
server = smtplib.SMTP("smtp.gmail.com", 587)

# Puts the SMTP connection in TLS (Transport Layer Security Mode
# All SMTP commands that follow will be encrypted
server.starttls()

# Login using your Gmail address and password
server.login()"""email, password """

"""
Use the SMS gateway provided by your mobile carrier:

AT&T:        number@mms.att.net
T-Mobile:    number@tmomail.net
Verizon:     number@vtext.com
Sprint:      number@page.nextel.com

Replace the number prefix with your phone number.
"""

"""
Message details

sender can be anything, but the text message will always show as
being send from your Gmail address.

receiver must be in the format of the SMS gateway provided by your
mobile carrier above. Example: 5555555555@vtext.com

body is the actual contents of the message
"""

image_path = '/home/pi/Desktop/image.jpg'
sender = "send email"
receiver = "reciever email"

def takePicture():
    camera.capture(image_path)
    sendText()

# Message creation
# This message format must be used because message headers must be included
# A subject header can also be used after the To header
def sendText():
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
    #loop that keeps polling the pins
    while(1):
        if pir.motion_detected: # if the pins status changes we enter this if
            localTime = time.localtime(time.time()) # gets local time stamp
            print("Motion detected " , localTime) # prints notification
            takePicture()
            time.sleep(10) # wait for ten secs

        else: # if state unchanged we enter this condition
            print("No Motion detected") # simple print
            time.sleep(1) # sleep for one sec
            
def main():
    detectMotion()

main()

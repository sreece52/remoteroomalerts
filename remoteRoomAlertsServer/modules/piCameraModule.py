from picamera import PiCamera
import emailModule
from emailModule import Email

class Camera:

   image_path = '/home/pi/github/remoteroomalerts/remoteRoomAlertsServer/static/photos/image.jpg'

   def __init__(self):
      # image variable
      self.email = Email() # email instance variable
   
   def takePicture(self):
      cam = PiCamera() # camera object
      cam.rotation = 90 # change this variable to rotate camera
      cam.capture(Camera.image_path) # tell camera to take picture
      print("Picture taken")
      self.email.sendEmail(Camera.image_path) # tell email module to send an email
      cam.close() # release camera resources

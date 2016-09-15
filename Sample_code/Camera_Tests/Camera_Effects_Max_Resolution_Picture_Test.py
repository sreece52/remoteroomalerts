from picamera import PiCamera
from time import sleep

camera = PiCamera()

#Image can be rotated by 90, 180, 270 degrees, or 0 to reset
camera.rotation = 180

"""
The camera's resolution can be changed. The max resolution for pictures
is 2592 x 1944. For videos, it is 1920 x 1080.  The default resolution
is set to whatever your monitor's resolution is. For the max picture
resolution, the framerate needs to be set to 15.
"""
camera.resolution = (2592, 1944)
camera.framerate = 15

#Preview only works if Pi is connected to a monitor
#An alpha level can be passed to start_preview to alter the transparency of the preview (0-255)
#camera.start_preview(alpha = 200)
camera.start_preview()

#Sleep for at least 2 seconds to allow the sensor to set its light levels
sleep(5)

#The path passed to capture is where the picture is saved
camera.capture("/home/pi/Desktop/max.jpg")
    
camera.stop_preview()

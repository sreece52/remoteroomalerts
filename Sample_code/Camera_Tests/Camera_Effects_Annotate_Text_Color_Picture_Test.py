from picamera import PiCamera, Color
from time import sleep

camera = PiCamera()

#Image can be rotated by 90, 180, 270 degrees, or 0 to reset
camera.rotation = 180

#Preview only works if Pi is connected to a monitor
#An alpha level can be passed to start_preview to alter the transparency of the preview (0-255)
#camera.start_preview(alpha = 200)
camera.start_preview()

"""
The annotation text's background and foreground color can be
altered using the Color library from picamera
"""
camera.annotate_background = Color("blue")
camera.annotate_foreground = Color("yellow")
#Text can be added to an image using annotate_text
camera.annotate_text = "Hello world!"

#Sleep for at least 2 seconds to allow the sensor to set its light levels
sleep(5)

#The path passed to capture is where the picture is saved
camera.capture("/home/pi/Desktop/text.jpg")
    
camera.stop_preview()

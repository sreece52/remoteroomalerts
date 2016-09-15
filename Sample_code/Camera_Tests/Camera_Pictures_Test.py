from picamera import PiCamera
from time import sleep

camera = PiCamera()

#Image can be rotated by 90, 180, 270 degrees, or 0 to reset
camera.rotation = 180

#Preview only works if Pi is connected to a monitor
#An alpha level can be passed to start_preview to alter the transparency of the preview (0-255)
#camera.start_preview(alpha = 200)
camera.start_preview()

#Takes 5 pictures
for i in range(5):
    #Sleep for at least 2 seconds to allow the sensor to set its light levels
    sleep(5)

    #The path passed to capture is where the picture is saved
    camera.capture("/home/pi/Desktop/image%s.jpg" % i)
    
camera.stop_preview()

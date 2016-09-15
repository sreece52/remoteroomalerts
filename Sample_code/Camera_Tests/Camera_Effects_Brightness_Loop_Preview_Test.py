from picamera import PiCamera
from time import sleep

camera = PiCamera()

#Image can be rotated by 90, 180, 270 degrees, or 0 to reset
camera.rotation = 180

#Preview only works if Pi is connected to a monitor
#An alpha level can be passed to start_preview to alter the transparency of the preview (0-255)
#camera.start_preview(alpha = 200)
camera.start_preview()

# The for loop displays and increases the brightness of the preview
for i in range(100):
    camera.annotate_text = "Brightness: %s" % i
    camera.brightness = i
    sleep(0.1)
    
camera.stop_preview()

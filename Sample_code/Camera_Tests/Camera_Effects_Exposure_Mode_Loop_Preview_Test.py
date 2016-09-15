from picamera import PiCamera
from time import sleep

camera = PiCamera()

#Image can be rotated by 90, 180, 270 degrees, or 0 to reset
camera.rotation = 180

#Preview only works if Pi is connected to a monitor
#An alpha level can be passed to start_preview to alter the transparency of the preview (0-255)
#camera.start_preview(alpha = 200)
camera.start_preview()

"""
exposure_mode can set the exposure to a preset mode to apply a particular effect.
The optoins are: off, auto, night, nightpreview, backlight, spotlight,
sports, snow, beach, verylong, fixedfps, antishake, and fireworks. The
default is auto.
"""
#The for loop displays and changes the exposure_mode throughout the preview
for mode in camera.EXPOSURE_MODES:
    camera.exposure_mode = mode
    camera.annotate_text = "Exposure mode: %s" % mode
    sleep(5)
    
camera.stop_preview()

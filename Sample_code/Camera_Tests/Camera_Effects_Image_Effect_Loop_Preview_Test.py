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
image_effect can be used to add a large variety of image effects.
The options are: none, negative, solarize, sketch, denoise, emboss,
oilpaint, hatch, gpen, pastel, watercolor, film, blur, saturation,
colorswap, washedout, posterise, colorpoint, colorbalance, cartoon,
deinterlace1, and deinterlace2. The default is none.
"""
#The for loop displays and changes the image_effect throughout the preview
for effect in camera.IMAGE_EFFECTS:
    camera.image_effect = effect
    camera.annotate_text = "Effect: %s" % effect
    sleep(5)
    
camera.stop_preview()

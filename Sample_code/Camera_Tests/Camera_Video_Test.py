from picamera import PiCamera
from time import sleep

camera = PiCamera()

#Image can be rotated by 90, 180, 270 degrees, or 0 to reset
camera.rotation = 180

#Preview only works if Pi is connected to a monitor
#An alpha level can be passed to start_preview to alter the transparency of the preview (0-255)
#camera.start_preview(alpha = 200)
camera.start_preview()

#The path passed to start_recording is where the video is saved
camera.start_recording("/home/pi/Desktop/video.h264")
#Record for 10 seconds
sleep(10)
camera.stop_recording()

camera.stop_preview()

"""
To play the video, open the terminal and travel to the directory
that the video is stored in. Then, use the following command:
omxplayer video.h264
The video may seem to playback faster due to omxplayer's
fast frame rate.
"""

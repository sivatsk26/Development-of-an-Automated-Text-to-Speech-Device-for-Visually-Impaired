from picamera2 import Picamera2, Preview
import time
from datetime import datetime
from gpiozero import Button
from signal import pause
picam2 = Picamera2()
button = Button(17)
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
def capture():
    picam2.start_preview(Preview.QT)
    timestamp = datetime.now().isoformat()
    picam2.start()
    time.sleep(2)
    picam2.capture_file('/home/pi/%s.jpg' % timestamp)
    picam2.stop_preview()
    picam2.stop()
button.when_pressed = capture
pause()

'''''
from picamera2 import Picamera2
from libcamera import controls
import os
picam2 = Picamera2()
os.system("v4l2-ctl --set-ctrl wide_dynamic_range=1 -d /dev/v4l-subdev0")
print("Setting HDR to ON")
picam2.start(show_preview=True)
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous, "AfSpeed": controls.AfSpeedEnum.Fast})
picam2.start_and_capture_files("HDRfastfocus{:d}.jpg", num_files=3, delay=1)
picam2.stop_preview()
picam2.stop()
print("Setting HDR to OFF")
os.system("v4l2-ctl --set-ctrl wide_dynamic_range=0 -d /dev/v4l-subdev0")
'''
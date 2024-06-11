from picamera2 import Picamera2, Preview
from libcamera import controls, Transform
import time
from pynput import keyboard

picam2 = Picamera2()
picam2.start_preview(Preview.QT)
camera_config = picam2.create_still_configuration(main={"size":(1920,1080)},lores={"size":(640,480)},display="lores")
picam2.configure(camera_config)
#Continuous focus
#picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
#Manually adjust lens position
#picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 10.0})
#Fast focus
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous, "AfSpeed": controls.AfSpeedEnum.Fast})
picam2.title_fields = ["ExposureTime", "AnalogueGain"]
picam2.start(show_preview=True)

def on_press(key):
    try:
        if key.char == "s":
            picam2.capture_file("teste.jpg")
            print("Image captured!")
            return False
        elif key.char == "q":
            return False
    except AttributeError:
        pass

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

picam2.stop_preview()

'''''
from picamera2 import Picamera2, Preview
from libcamera import controls, Transform
import time
import keyboard

picam2 = Picamera2()
picam2.start_preview(Preview.QT)
camera_config = picam2.create_still_configuration(main={"size":(1920,1080)},lores={"size":(640,480)},display="lores")
picam2.configure(camera_config)
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
picam2.title_fields = ["ExposureTime", "AnalogueGain"]
picam2.start(show_preview=True)

while True:
    event = keyboard.read_event()
    if event.name == "s" and event.event_type == "down":
        picam2.capture_file("test.jpg")
        print("Image captured!")
        break
    elif event.name == "q" and event.event_type == "down":
        break

picam2.stop_preview()
'''
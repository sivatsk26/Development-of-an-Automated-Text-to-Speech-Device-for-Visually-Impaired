import time
import RPi.GPIO as GPIO
from picamera2 import Picamera2, Preview
from libcamera import controls, Transform

picam2 = Picamera2()
picam2.start_preview(Preview.QT)
camera_config = picam2.create_still_configuration(main={"size":(1920,1080)},lores={"size":(640,480)},display="lores")
picam2.configure(camera_config)
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous, "AfSpeed": controls.AfSpeedEnum.Fast})
picam2.title_fields = ["ExposureTime", "AnalogueGain"]
picam2.start(show_preview=True)

BUTTON_PIN_CA = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN_CA, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(BUTTON_PIN_CA)
    if input_state == GPIO.LOW:
        picam2.capture_file("teste.jpg")
        print("Image captured!")
        picam2.stop()
        GPIO.cleanup()
        break
    time.sleep(0.1)

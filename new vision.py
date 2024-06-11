import cv2
import os
import io
import RPi.GPIO as GPIO
from time import sleep
from google.cloud import vision_v1
from google.cloud.vision_v1 import types

# Set up credentials for Google Cloud APIs
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "refreshing-park-380803-5c8ce97dd8f0.json"

# Initialize clients for Google Cloud APIs
client_vision = vision_v1.ImageAnnotatorClient()

# Initialize the button press counter
button_presses = 0

# Set up GPIO pin for button
button_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define a function to handle button press events
def button_press(channel):
    global button_presses
    button_presses += 1
    if button_presses == 1:
        # Set the language option to English
        image_context = types.ImageContext(language_hints=["en"])
        print("Language option set to English.")
    elif button_presses == 2:
        # Set the language option to Tamil
        image_context = types.ImageContext(language_hints=["ta"])
        print("Language option set to Tamil.")
    else:
        # Reset the button press counter if more than two presses
        button_presses = 0
        # Set the language option to the default (no language hint)
        image_context = types.ImageContext()
        print("Language option set to default (no language hint).")
    return image_context

# Set up GPIO event detection for button press
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_press, bouncetime=300)

while True:
    # Read the image file using cv2.imread() and convert it to JPEG format using cv2.imencode()
    img = cv2.imread('/home/sk2/Documents/Vision ocr/Capture_8.jpeg')
    img_bytes = cv2.imencode('.jpg', img)[1].tobytes()
    # Create a types.Image object from the JPEG-encoded image bytes
    image = types.Image(content=img_bytes)
    # Call the OCR function with the language option set by the button_press function
    response = client_vision.document_text_detection(image=image, image_context=button_press(None))
    # Extract the OCR result from the response
    text = response.full_text_annotation.text
    print(text)
    # Reset the button press counter to zero after the third press
    if button_presses == 3:
        button_presses = 0
    # Wait for a moment before checking for button press again
    sleep(0.1)

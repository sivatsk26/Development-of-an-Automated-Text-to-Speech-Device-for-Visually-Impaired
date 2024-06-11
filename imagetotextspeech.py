#import picamera
import cv2
import os
from pydub import AudioSegment
from pydub.playback import play
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from googletrans import Translator
from google.cloud import texttospeech_v1 as texttospeech

# Set up credentials for Google Cloud APIs
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "refreshing-park-380803-5c8ce97dd8f0.json"
# Initialize clients for Google Cloud APIs
client_vision = vision_v1.ImageAnnotatorClient()
translator = Translator()
client_texttospeech = texttospeech.TextToSpeechClient()
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

BUTTON_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(BUTTON_PIN)
    if input_state == GPIO.LOW:
        picam2.capture_file("test.jpg")
        print("Image captured!")
        picam2.stop()
        GPIO.cleanup()
        break
    time.sleep(0.1)
# Load image using OpenCV
img = cv2.imread('/home/sk2/Documents/Vision ocr/test.jpg')
# Convert image to bytes
img_bytes = cv2.imencode('.jpg', img)[1].tobytes()
# Create a Vision API image object
image = types.Image(content=img_bytes)
# Set language hint to Tamil
image_context = types.ImageContext(language_hints=['en'])
# Detect text in the image
response = client_vision.document_text_detection(image=image, image_context=image_context)
texts = response.full_text_annotation.text
print("Extracted text: ",texts)
if len(texts) > 0:
# Get the detected text and translate it to a different language
    translated_text = translator.translate(texts, dest='en').text
    print("Translated text: ",translated_text)
    # Use Google Text-to-Speech to generate an audio file of the translated text
    synthesis_input = texttospeech.SynthesisInput(text=texts)
    voice = texttospeech.VoiceSelectionParams(language_code="en-IN", name="en-IN-Standard-D")
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client_texttospeech.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    # Save the audio file to disk
    with open("translated_text.mp3", "wb") as f:
        f.write(response.audio_content)
        print(f"Generated audio written to file 'translated_text.mp3'.")
else:
    print("No text detected in the image.")
song = AudioSegment.from_mp3("translated_text.mp3")
print('playing')
play(song)
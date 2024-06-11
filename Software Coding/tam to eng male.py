import cv2
import os,io
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from googletrans import Translator
from google.cloud import texttospeech_v1 as texttospeech
from picamera2 import Picamera2, Preview
from libcamera import controls, Transform
import time
from pynput import keyboard
from pydub import AudioSegment
from pydub.playback import play
# Set up credentials for Google Cloud APIs
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "refreshing-park-380803-5c8ce97dd8f0.json"
# Initialize clients for Google Cloud APIs
client_vision = vision_v1.ImageAnnotatorClient()
translator = Translator()
client_texttospeech = texttospeech.TextToSpeechClient()
picam2 = Picamera2()
picam2.start_preview(Preview.QT)
camera_config = picam2.create_still_configuration(main={"size":(1920,1080)},lores={"size":(640,480)},display="lores")
picam2.configure(camera_config)
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
picam2.title_fields = ["ExposureTime", "AnalogueGain"]
picam2.start(show_preview=True)

def on_press(key):
    try:
        if key.char == "s":
            picam2.capture_file("tatoen.jpg")
            print("Image captured!")
            return False
        elif key.char == "q":
            return False
    except AttributeError:
        pass

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
picam2.stop_preview()
# Load image using OpenCV
img = cv2.imread('/home/sk2/Documents/Vision ocr/tatoen.jpg')
# Convert image to bytes
img_bytes = cv2.imencode('.jpg', img)[1].tobytes()
# Create a Vision API image object
image = types.Image(content=img_bytes)
# Set language hint to English
image_context = types.ImageContext(language_hints=['ta'])
# Detect text in the image
response = client_vision.document_text_detection(image=image, image_context=image_context)
texts = response.full_text_annotation.text
print(texts)
if len(texts) > 0:
# Get the detected text and translate it to a different language
    translated_text = translator.translate(texts, dest='en').text
    print(translated_text)
    # Use Google Text-to-Speech to generate an audio file of the translated text
    synthesis_input = texttospeech.SynthesisInput(text=translated_text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-IN", name="en-IN-Standard-C")
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client_texttospeech.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    # Save the audio file to disks
    with open("tatoen translated_text.mp3", "wb") as f:
        f.write(response.audio_content)
        print(f"Audio content written to file 'tatoen translated_text.mp3'.")
song = AudioSegment.from_mp3("tatoen translated_text.mp3")
print('playing')
play(song)
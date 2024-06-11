import cv2
import time
import RPi.GPIO as GPIO
from picamera2 import Picamera2, Preview
from libcamera import controls, Transform
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from googletrans import Translator
import os
from google.cloud import texttospeech_v1 as texttospeech
from pydub import AudioSegment
from pydub.playback import play
# Set up credentials for Google Cloud APIs
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "refreshing-park-380803-5c8ce97dd8f0.json"

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

# Define a dictionary of language codes and their corresponding language hints and full names
language_options = {
    'en': {'hints': ['en'], 'name': 'english'},
    'ta': {'hints': ['ta'], 'name': 'tamil'},
    # Add more language codes, hints, and names as needed
}
# Prompt the user to select a language option
print('Select a language option:')
for key, value in language_options.items():
    print(f"{key}: {value['name']} ({', '.join(value['hints'])})")
language_code = input('Enter the language code: ')
if language_code not in language_options:
    print('Invalid language code')
else:
    # Create a client object using the service account credentials stored in a JSON file
    client_vision = vision_v1.ImageAnnotatorClient()
    # Read the image file using cv2.imread() and convert it to JPEG format using cv2.imencode()
    img = cv2.imread('/home/sk2/Documents/Vision ocr/test.jpg')
    img_bytes = cv2.imencode('.jpg', img)[1].tobytes()
    # Create a types.Image object from the JPEG-encoded image bytes
    image = types.Image(content=img_bytes)
    # Create an image_context object and set the language_hints parameter based on the selected language option
    language_hint = language_options[language_code]['hints']
    image_context = types.ImageContext(language_hints=language_hint)
    # Call the client.document_text_detection() method to perform OCR on the image
    response = client_vision.document_text_detection(image=image, image_context=image_context)
    # Extract the text from the response using the full_text_annotation.text attribute
    text = response.full_text_annotation.text
    # Prompt the user to select a translation option
    translate_option = input('Do you want to translate the text? (y/n): ')
    if translate_option.lower() == 'y':
        # Create a translator object
        translator = Translator()
        if language_code =='en':
            # Prompt the user to enter a destination language code
            dest_lang = 'ta'
        else:
            dest_lang = 'en'
        if language_code =='ta':
            dest_lang = 'en'
        else:
            dest_lang= 'ta'
        # Translate the text to the destination language
        translated_text = translator.translate(text, dest=dest_lang).text
        # Print the extracted text and translated text
        print(f"Extracted text: {text}")
        print(f"Translated text: {translated_text}")
        # Use Google Text-to-Speech to generate an audio file of the translated text
        synthesis_input = texttospeech.SynthesisInput(text=translated_text)        
    else:
        translate_option.lower() == 'n'
        # Create a translator object
        translator = Translator()
        if language_code =='en':
            # Prompt the user to enter a destination language code
            dest_lang = 'en'
        else:
            dest_lang = 'ta'
        if language_code =='ta':
            dest_lang = 'ta'
        else:
            dest_lang= 'en'
        # Translate the text to the destination language
        translated_text = translator.translate(text, dest=dest_lang).text
        # Print the extracted text only
        print(f"Extracted text: {text}")
        print(f"Translated text: {translated_text}")
        # Use Google Text-to-Speech to generate an audio file of the translated text
        synthesis_input = texttospeech.SynthesisInput(text=translated_text)
    # Set up the TextToSpeechClient object
    client_texttospeech = texttospeech.TextToSpeechClient()
    if dest_lang == 'en':
        language_code_tts ="en-IN"
        voice_name ="en-IN-Standard-D"
    else:
        dest_lang == 'ta'
        language_code_tts ="ta-IN"
        voice_name ="ta-IN-Standard-C"
    # Set the voice selection parameters based on user input
    voice = texttospeech.VoiceSelectionParams(language_code=language_code_tts,name =voice_name)
    # Set the audio configuration to use MP3 encoding
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    # Synthesize the speech and save the audio file to disk
    response = client_texttospeech.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    with open("translated_text.mp3", "wb") as f:
        f.write(response.audio_content)
        print(f"Audio content written to file 'translated_text.mp3'.")
song = AudioSegment.from_mp3("translated_text.mp3")
print('playing')
play(song)

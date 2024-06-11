import io
import os
import wave
# Import the necessary libraries
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
# Set up credentials for Google Cloud APIs
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "refreshing-park-380803-5c8ce97dd8f0.json"
# Set up the client object for the Speech-to-Text API
client = speech.SpeechClient()
# Set up the Google Cloud Storage URI of the audio file
audio_uri = 'gs://demo_bucket1234567/translated_text.wav'
audio = types.RecognitionAudio(uri = audio_uri)
config = types.RecognitionConfig(
    encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
    language_code='en-IN')
# transcribe the audio file
operation = client.long_running_recognize(config=config, audio=audio)
print('Waiting for operation to complete...')
response = operation.result(timeout=90)

# print the transcribed text
for result in response.results:
    print(result.alternatives[0].transcript)

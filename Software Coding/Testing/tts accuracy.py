from google.cloud import texttospeech_v1 as texttospeech
import os
import numpy as np
import soundfile as sf
# Set up credentials for Google Cloud APIs
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "refreshing-park-380803-5c8ce97dd8f0.json"
# create a client object
client_texttospeech = texttospeech.TextToSpeechClient()

# define the input text
input_text = "The quick brown fox jumps over the lazy dog."
'''''
synthesis_input = texttospeech.SynthesisInput(text=input_text)
voice = texttospeech.VoiceSelectionParams(language_code="en-IN", name="en-IN-Standard-C")
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
response = client_texttospeech.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

# write the audio file to disk
with open('generated_audio.mp3', 'wb') as out:
    out.write(response.audio_content)
'''
# load the expected audio file from disk
expected_audio, expected_sample_rate = sf.read('expected voice.mp3')

# load the generated audio file from disk
generated_audio, generated_sample_rate = sf.read('generated_audio.mp3')

# check the sample rates
if expected_sample_rate != generated_sample_rate:
    # resample the audio to a common sample rate
    if expected_sample_rate < generated_sample_rate:
        generated_audio, generated_sample_rate = sf.resample(generated_audio, generated_sample_rate, expected_sample_rate)
    else:
        expected_audio, expected_sample_rate = sf.resample(expected_audio, expected_sample_rate, generated_sample_rate)

# check the lengths
if len(expected_audio) != len(generated_audio):
    # trim the longer audio file to match the length of the shorter audio file
    if len(expected_audio) < len(generated_audio):
        generated_audio = generated_audio[:len(expected_audio)]
    else:
        expected_audio = expected_audio[:len(generated_audio)]

# calculate the accuracy
mse = np.mean((expected_audio - generated_audio) ** 2)
accuracy = 1 - np.sqrt(mse) / np.max(expected_audio)

# print the accuracy
print("Accuracy: {:.2f}%".format(accuracy * 100))
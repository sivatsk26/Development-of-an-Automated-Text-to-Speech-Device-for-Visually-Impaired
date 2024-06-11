import cv2
import os,io
from google.cloud import vision_v1 as vision
from googletrans import Translator
import langcodes
import nltk
# Set up credentials for Google Cloud APIs
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "refreshing-park-380803-5c8ce97dd8f0.json"

# Initialize clients for Google Cloud APIs
client_vision = vision.ImageAnnotatorClient()
translator = Translator()
# Split the text into sentences using the nltk library
nltk.download('punkt')
def split_into_sentences(text):
    sentences = nltk.sent_tokenize(text)
    return sentences

# Send the image to Google Cloud Vision for text detection and recognition
vfilename="Capture_8.jpeg"
vfilepath=f'/home/sk2/Documents/Vision ocr/{vfilename}'

with io.open(vfilepath,'rb') as image_nefile:
    content=image_nefile.read()

image=vision.Image(content=content)
response = client_vision.document_text_detection(image=image)
texts = response.full_text_annotation.text
print("detected text",texts)
# Split the detected text into sentences
sentences = split_into_sentences(texts)
import re

# Define a regular expression to match only alphanumeric characters and spaces
regex = re.compile('[^a-zA-Z0-9\s]')

# Split the detected text into sentences and filter out non-textual characters
sentences = [regex.sub('', sentence.strip()) for sentence in split_into_sentences(texts)]

# Loop through each sentence and print its language if it is a valid language code tag
for sentence in sentences:
    try:
        language_code = langcodes.get(sentence).language
        language_name = langcodes.get(language_code).language_name()
        print(f"Sentence '{sentence}' is in {language_name} ({language_code})")
    except langcodes.LanguageTagError:
        print(f"Unable to detect language for sentence '{sentence}'")

if len(texts) > 0:
# Get the detected text and translate it to a different language
    translated_text = translator.translate(texts, dest='ta').text
    print("translated text",translated_text)
    
import cv2
import os,io
from google.cloud import vision_v1 as vision
from google.cloud import translate_v2 as translate

# Set up credentials for Google Cloud APIs
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "refreshing-park-380803-5c8ce97dd8f0.json"

# Initialize clients for Google Cloud APIs
client_vision = vision.ImageAnnotatorClient()
client_translate = translate.Client()
'''''
# Set up the webcam
camera=cv2.VideoCapture(1)
count = 1
while True:
    _,image=camera.read()
    cv2.imshow('image',image)
    if cv2.waitKey(1)& 0xFF==ord('s'):
        cv2.imwrite('test1.jpg',image)
        break
camera.release()
cv2.destroyAllWindows()
'''
# Send the image to Google Cloud Vision for text detection and recognition
vfilename="Capture_14.jpeg"
vfilepath=f'C:/Users/ELCOT/Vision ocr/{vfilename}'

with io.open(vfilepath,'rb') as image_nefile:
    content=image_nefile.read()

image=vision.Image(content=content)
response = client_vision.text_detection(image=image)
texts = response.text_annotations
print(texts)
if len(texts) > 0:
# Get the detected text and translate it to a different language
    detected_text = texts[0].description
    translated_text = client_translate.translate(detected_text, target_language="en")["translatedText"]
    print(translated_text)

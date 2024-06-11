import cv2
from google.cloud import vision_v1
from google.cloud.vision_v1 import types

# Authenticate with Google Cloud Vision API
client = vision_v1.ImageAnnotatorClient.from_service_account_json('C:/Users/ELCOT/Vision ocr/refreshing-park-380803-5c8ce97dd8f0.json')
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
# Load image using OpenCV
img = cv2.imread('C:/Users/ELCOT/Vision ocr/Capture_8.jpeg')
# Convert image to bytes
img_bytes = cv2.imencode('.jpg', img)[1].tobytes()
# Create a Vision API image object
image = types.Image(content=img_bytes)
# Set language hint to Tamil
image_context = types.ImageContext(language_hints=['ta'])
# Detect text in the image
response = client.document_text_detection(image=image, image_context=image_context)
text = response.full_text_annotation.text
print(text)
pages = response.full_text_annotation.pages
for page in pages:
    for block in page.blocks:
        print('block confidence:{}'.format(block.confidence))
        for paragraph in block.paragraphs:
            print('paragraph confidence:{}'.format(paragraph.confidence))
        
            for word in paragraph.words:
                word_text =''.join([symbol.text for symbol in word. symbols])
                print('Word text: {} (confidence: {})'.format (word_text, word.confidence))
                for symbol in word.symbols:
                    print('\tSymbol: {} (confidence: {})'.format(symbol.text, symbol.confidence))
    
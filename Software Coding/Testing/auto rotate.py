'''''
import cv2
import numpy as np
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
# Authenticate with Google Cloud Vision API
client = vision_v1.ImageAnnotatorClient.from_service_account_json('C:/Users/ELCOT/Vision ocr/refreshing-park-380803-5c8ce97dd8f0.json')
# Load image using OpenCV
img = cv2.imread(r'C:/Users/ELCOT/Vision ocr/Capture_81.jpeg')
# Deskew image
coords = np.column_stack(np.where(img.sum(axis=2)>=300))
angle = 90 - cv2.minAreaRect(coords)[-1]
if angle < -45:
    angle = -(90 + angle)
else:
    angle = -angle
(h, w) = img.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
# Convert image to bytes
img_bytes = cv2.imencode('.jpg', img)[1].tobytes()
cv2.imshow('Text Detection', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Create a Vision API image object
image = types.Image(content=img_bytes)
# Set language hint to Tamil
image_context = types.ImageContext(language_hints=['en'])
# Detect text in the image
response = client.document_text_detection(image=image, image_context=image_context)
text = response.full_text_annotation.text
print(text)
'''

import cv2
import numpy as np
img = cv2.imread('C:/Users/ELCOT/Vision ocr/Capture_81.jpeg')
def deskew(img):
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Threshold the image to binary to make it easier to detect lines
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Detect lines using the Hough transform
    lines = cv2.HoughLinesP(thresh, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)[0]
    
    # Compute the angle of the dominant line
    angles = []
    for x1, y1, x2, y2 in lines:
        angle = np.arctan2(y2 - y1, x2 - x1) * 540 / np.pi
        angles.append(angle)
    angle = np.median(angles)
    
    # Rotate the image using the angle of rotation
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    return rotated
deskewed = deskew(img)
cv2.imshow('Text Detection', deskewed)
cv2.waitKey(0)
cv2.destroyAllWindows()

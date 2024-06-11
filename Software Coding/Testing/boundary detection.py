import io
import cv2
from google.cloud import vision_v1
from google.cloud.vision_v1 import types

# Authenticate with Google Cloud Vision API
client = vision_v1.ImageAnnotatorClient.from_service_account_json('C:/Users/ELCOT/Vision ocr/refreshing-park-380803-5c8ce97dd8f0.json')

# Load image using OpenCV
img = cv2.imread('C:/Users/ELCOT/Vision ocr/Capture_10.jpg')
# Increase image resolution
img = cv2.resize(img, None, fx=1, fy=1)
# Enhance contrast
#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
#img = cv2.equalizeHist(img)

# Remove noise
#img = cv2.medianBlur(img, 3)

# Thresholding
#_, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# Convert image to bytes
img_bytes = cv2.imencode('.jpg', img)[1].tobytes()
#cv2.imshow('Text Detection', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# Create a Vision API image object
image = types.Image(content=img_bytes)

# Detect text in the image
response = client.text_detection(image=image)
annotations = response.text_annotations
text = response.full_text_annotation.text
print(text)
texts = response.text_annotations
# Draw boundary boxes and contour text on the image
for annotation in annotations[1:]:
    vertices = [(vertex.x, vertex.y) for vertex in annotation.bounding_poly.vertices]
    img = cv2.rectangle(img, vertices[0], vertices[2], (0, 255, 0), 1)
    img = cv2.putText(img, annotation.description, vertices[0], cv2.FONT_HERSHEY_TRIPLEX, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
# Shows the resulting image
cv2.imshow('Text Detection', img)
cv2.imwrite('Boundary Detected1.jpg',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

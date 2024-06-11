import cv2
from google.cloud import vision_v1
from google.cloud.vision_v1 import types

# Authenticate with Google Cloud Vision API
client = vision_v1.ImageAnnotatorClient.from_service_account_json('C:/Users/ELCOT/Vision ocr/refreshing-park-380803-5c8ce97dd8f0.json')
# Load image using OpenCV
img = cv2.imread('C:/Users/ELCOT/Vision ocr/Capture_13.jpeg')
# Convert image to bytes
img_bytes = cv2.imencode('.jpg', img)[1].tobytes()
# Create a Vision API image object
image = types.Image(content=img_bytes)
# Set language hint to Tamil
image_context = types.ImageContext(language_hints=['ta'])
# Detect text in the image
response = client.document_text_detection(image=image, image_context=image_context)
text = response.full_text_annotation.text
# define the expected translation
expected_text = "ஒரு குட்டிக் கதை தையற்காரர் ஒருவர்,தனது கடையில் துணிகள் தைத்துக்கொண்டிருந்தார். அவருடைய மகன் அருகில் இருந்து, அவர் வேலை செய்வதைப் பார்த்துக் கொண்டிருந்தான். தையற்காரர் ஒரு புதுத் துணியை எடுத்தார். அதை அழகிய பளபளக்கும் கத்திரிக்கோலால் துண்டுகளாக வெட்டினார். பின்னர் கத்திரிக்கோலைக் கால் அருகே போட்டுவிட்டு துணியைத் தைக்கலானார். துணியை தைத்து முடிந்ததும் சிறிய ஊசியை எடுத்துத் தனது தலையில் இருந்த தொப்பியில் குத்திப் பத்திரப்படுத்தினார். இதைப் பார்த்துக் கொண்டிருந்த மகன் அவரிடம், அப்பா ! கத்திரிகோல் விலை உயர்ந்தது, அழகானது. அதை அலட்சியமாக காலடியில் போடுகிறீர்கள். ஊசி சிறியது மலிவானது. ஆனால், அதை தலையில் பாதுகாக்கிறீர்களே. அது ஏன்...? என்று கேட்டான். நீ சொல்வது உண்மைதான் என்றார் தையற்காரர். கத்திரிகோல் அழகாகவும் மதிப்புள்ளதாகவும் இருந்தாலும், அதன் செயல் வெட்டுவது.அதாவது பிரிப்பது! ஆனால், ஊசி சிறியதாகவும், மலிவானதாகவும் இருந்தாலும் அதன் செயல் சேர்ப்பது. ஒருவருடைய மதிப்பு அவருடைய செயலைக்கொண்டே நிர்ணயிக்கப்படுகிறது. அவர் உருவத்தை வைத்து அல்ல. நல்லதையே செய்வோம்! நல்லவர்களாக வாழ்வோம்!"
# calculate the translation accuracy
accuracy = len(set(text.split()) & set(expected_text.split())) / len(set(expected_text.split())) * 100

# print the translation and accuracy
print("Original text: ", text)
print("Expected text: ", expected_text)
print("Accuracy: {:.2f}%".format(accuracy))
import os
from google.cloud import translate_v2 as translate

# Set the credentials environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "refreshing-park-380803-5c8ce97dd8f0.json"

# Initialize the client for Cloud Translation API
client_translate = translate.Client()

# Example usage of Cloud Translation API
text = 'Hello, world!'
target_language = 'ta'
result = client_translate.translate(text, target_language=target_language)
print(result['input'], '->', result['translatedText'])
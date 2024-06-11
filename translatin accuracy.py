from googletrans import Translator

# create a Translator object
translator = Translator()

# define the text to be translated
text_to_translate = "life could be wonderful if people would leave you alone. Laughter if people would leave you alone. Laugher is the"
# translate the text to French
translated_text = translator.translate(text_to_translate, dest='ta').text

# define the expected translation
expected_translation = "The quick brown fox jumps over the lazy dog."

# calculate the translation accuracy
accuracy = len(set(translated_text.split()) & set(expected_translation.split())) / len(set(expected_translation.split())) * 100

# print the translation and accuracy
print("Original text: ", text_to_translate)
print("Translated text: ", translated_text)
print("Expected translation: ", expected_translation)
print("Translation accuracy: {:.2f}%".format(accuracy))
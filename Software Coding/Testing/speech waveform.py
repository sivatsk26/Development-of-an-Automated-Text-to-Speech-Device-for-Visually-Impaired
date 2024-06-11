import librosa
import librosa.display
import matplotlib.pyplot as plt

# Load speech signal
signal, sr = librosa.load('C:/Users/ELCOT/Vision ocr/expected voice.mp3')

# Visualize waveform
plt.figure(figsize=(12, 4))
librosa.display.waveshow(signal, sr=sr)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Speech Waveform')
plt.show()
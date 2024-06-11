from pydub import AudioSegment
from pydub.playback import play
song = AudioSegment.from_mp3("translated_text.mp3")
print('playing')
play(song)
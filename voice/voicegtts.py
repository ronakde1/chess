from gtts import gTTS
import os

# Text to be converted to speech
text = "Hello, I am Jarvis, at your service."

# Language and settings
language = 'en'  # Use 'en' for English

# Generate the speech
tts = gTTS(text=text, lang=language, slow=False)  # slow=False for a normal speed voice

# Save the audio file
tts.save("jarvis_voice.mp3")

# Play the audio file
os.system("open jarvis_voice.mp3")  # 'start' for Windows, use 'open' for macOS or 'xdg-open' for Linux

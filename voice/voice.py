import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Get and set an American-sounding voice
voices = engine.getProperty('voices')
for voice in voices:
    if "en_US" in voice.id:  # Look for an American English voice
        engine.setProperty('voice', voice.id)
        break

# Set speech rate
engine.setProperty('rate', 150)  # You can adjust this to make the voice sound smoother

# Set volume
engine.setProperty('volume', 0.9)  # Volume: 0.0 to 1.0

# Text to be spoken
text = "Hello, I am Jarvis, at your service."

# Speak the text
engine.say(text)
engine.runAndWait()

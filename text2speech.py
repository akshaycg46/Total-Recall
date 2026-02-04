import pyttsx3

def text_to_speech(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set properties before adding anything to speak
    engine.setProperty('rate', 150)    # Speed of speech
    engine.setProperty('volume', 0.9)  # Volume 0-1

    # Speak the text
    engine.say(text)

    # Blocks while processing all the currently queued commands
    engine.runAndWait()

if __name__ == "__main__":
    # Example text
    text = "Hello, how can I assist you today?"
    # Convert and play the text
    text_to_speech(text)
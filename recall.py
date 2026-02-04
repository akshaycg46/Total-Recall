import speech_recognition as sr
from transformers import AutoTokenizer, AutoModel
import torch

from p2 import total_recall
from llm import process_prompt
from text2speech import text_to_speech

def main():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Initialize the microphone
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        
        # Capture audio from the microphone
        audio = recognizer.listen(source)
        print("Processing...")
        
        try:
            # Recognize the speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
                        
            result = total_recall(text)
            print("result =============> ", result)
            text_to_speech(result)
            # generated_response = process_prompt(result)
            # text_to_speech(generated_response)
            

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    main()

!pip install gTTS
!pip install pydub simpleaudio
from gtts import gTTS
import os
from IPython.display import Audio
import os
from IPython.display import Audio

def text_to_speech_indian_english():
    """
    Converts user-input text to speech in Indian English using gTTS.
    """
    text = input("Enter the text you want to convert to Podcast: ")

    tld = 'co.uk'
    accent_name = "Indian English"

    try:
        print(f"\nGenerating speech in {accent_name}...")
        tts = gTTS(text=text, lang='en', tld=tld, slow=False)

        output_file = "podcast.mp3"
        tts.save(output_file)
        print(f"Speech saved to '{output_file}'")


        print("\nTo play the audio, open 'indian_speech.mp3' with your media player.")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have an active internet connection.")

if __name__ == "__main__":
    text_to_speech_indian_english()

Audio("podcast.mp3", autoplay=True)
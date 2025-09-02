!pip install gTTS
!pip install pydub simpleaudio
from gtts import gTTS
import os
from IPython.display import Audio
import os
from IPython.display import Audio

def text_to_speech_indian_english():
    """
    Converts user-input text to Podcast gTTS.
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

"""**Podcast from Docs**"""

!pip install python-docx
!pip install PyPDF2
!pip install pytesseract

import os
from docx import Document
import PyPDF2
from PIL import Image
import pytesseract
from gtts import gTTS
from IPython.display import Audio

def extract_text_from_file(file_path):
    """
    Extracts text from different file types (txt, docx, pdf, image).
    """
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    elif file_extension == '.docx':
        doc = Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    elif file_extension == '.pdf':
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text() or ""
        return text
    elif file_extension in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
        try:

            img = Image.open(file_path)
            return pytesseract.image_to_string(img)
        except Exception as e:
            print(f"Error processing image file {file_path}: {e}")
            print("Please ensure Tesseract OCR is installed and configured correctly.")
            return None
    else:
        return None

def generate_podcast_from_input():
    """
    Converts text from user-specified input (file or direct text) to an Indian English podcast.
    """
    while True:
        input_type = input("Do you want to enter text directly or provide a file path? (text/file): ").lower()
        if input_type in ['text', 'file']:
            break
        else:
            print("Invalid input. Please type 'text' or 'file'.")

    text_content = ""
    if input_type == 'text':
        text_content = input("Enter the text you want to convert to podcast: ")
    else:
        while True:
            file_path = input("Enter the path to the file (txt, docx, pdf, png, jpg, jpeg, gif, bmp): ")
            if not os.path.exists(file_path):
                print("File not found. Please enter a valid file path.")
            else:
                text_content = extract_text_from_file(file_path)
                if text_content is None:
                    print("Unsupported file type or error extracting text. Please try another file.")
                elif not text_content.strip():
                    print("No discernible text found in the file. Please check the file content or try a different file.")
                else:
                    break
        if not text_content:
            print("Could not extract text. Exiting.")
            return

    if not text_content.strip():
        print("No text provided or extracted to generate a podcast. Exiting.")
        return

    tld = 'co.in'
    accent_name = "Indian English"

    try:
        print(f"\nGenerating podcast in {accent_name}...")
        tts = gTTS(text=text_content, lang='en', tld=tld, slow=False)

        output_file = "podcast.mp3"
        tts.save(output_file)
        print(f"Podcast saved to '{output_file}'")

        print("\nPlaying the generated podcast...")
        display(Audio(output_file, autoplay=True))

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have an active internet connection and valid text.")

if __name__ == "__main__":
    generate_podcast_from_input()
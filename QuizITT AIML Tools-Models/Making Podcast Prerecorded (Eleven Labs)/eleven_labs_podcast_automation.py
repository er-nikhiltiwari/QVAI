!pip install requests

import requests
import IPython.display as ipd
import os

api_key = "sk_9f710a10d73ac41b6e2ba016b05cecf6277ed14ad227aed7"

voice_id = "Zjz30d9v1e5xCxNVTni6"

def text_to_speech(text, voice_id, api_key, output_filename="generated_audio.mp3"):
    """
    Converts text to speech using the ElevenLabs API.

    Args:
        text (str): The text to convert.
        voice_id (str): The ID of the voice to use.
        api_key (str): Your ElevenLabs API key.
        output_filename (str): The name of the output MP3 file.
    """
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    print(f"Generating speech for voice ID: {voice_id}...")
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        with open(output_filename, "wb") as f:
            f.write(response.content)
        print(f"Audio saved to '{output_filename}'")
        return output_filename
    except requests.exceptions.RequestException as e:
        print(f"Error generating speech: {e}")
        if response is not None:
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.text}")
        return None

if __name__ == "__main__":

    if api_key == "YOUR_ELEVENLABS_API_KEY" or voice_id == "YOUR_VOICE_ID":
        print("--- CONFIGURATION REQUIRED ---")
        print("Please replace 'YOUR_ELEVENLABS_API_KEY' and 'YOUR_VOICE_ID' in the code.")
        print("You can find your API key and voice IDs on the ElevenLabs website.")
        print("Exiting program.")
    else:

        print("--- Text-to-Speech Generator ---")
        input_text = input("Enter the text you want to convert to speech: ")

        if input_text:
            output_file = text_to_speech(input_text, voice_id, api_key, "generated_audio.mp3")

            if output_file and os.path.exists(output_file):
                print("\nPlaying the generated audio:")
                ipd.display(ipd.Audio(output_file))
            else:
                print("Audio generation failed or output file not found.")
        else:
            print("No text entered. Please provide some text to convert.")
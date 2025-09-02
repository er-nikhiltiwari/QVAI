import sounddevice as sd
import numpy as np
import speech_recognition as sr
from scipy.io.wavfile import write
import os
import json
from datetime import datetime

# === Config ===
TOTAL_DURATION = 16     # seconds
CHUNK_DURATION = 1     # seconds per chunk
SAMPLE_RATE = 44100
CHANNELS = 1
AUDIO_DIR = "audio_files"
OUTPUT_DIR = "outputs"
FULL_AUDIO_FILENAME = "audio.wav"
JSON_FILENAME = "transcription.json"

# === Paths ===
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
full_audio_path = os.path.join(AUDIO_DIR, FULL_AUDIO_FILENAME)
json_path = os.path.join(OUTPUT_DIR, JSON_FILENAME)

# === Init ===
recognizer = sr.Recognizer()
full_audio_data = []
full_transcript = ""

print(f"\n Start speaking. Live transcription begins...")

# === Live-like Chunked Recording & Transcription ===
for i in range(0, TOTAL_DURATION, CHUNK_DURATION):
    chunk = sd.rec(int(CHUNK_DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16')
    sd.wait()
    full_audio_data.append(chunk)

    # Save chunk to temp file
    temp_wav = "temp_chunk.wav"
    write(temp_wav, SAMPLE_RATE, chunk)

    # Transcribe the chunk
    try:
        with sr.AudioFile(temp_wav) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            full_transcript += " " + text
            print(f" {text}")
    except sr.UnknownValueError:
        print(" [Unrecognized speech]")
        full_transcript += " [Unrecognized]"
    except sr.RequestError:
        print(" [Google API Error]")
        full_transcript += " [API Error]"

# Save full audio
final_audio = np.concatenate(full_audio_data, axis=0)
write(full_audio_path, SAMPLE_RATE, final_audio)

# Save JSON transcription
output = {
    "timestamp": datetime.now().isoformat(),
    "audio_file": full_audio_path,
    "transcription": full_transcript.strip()
}

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

print(f"\n Transcription saved to: {json_path}")

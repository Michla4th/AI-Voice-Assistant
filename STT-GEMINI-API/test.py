import requests
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import time

# Flask server address (update if running on another machine)
SERVER_URL = "https://api.stemkul.com/upload"

DURATION = 5 
SAMPLE_RATE = 44100  
FILE_PATH = "recorded_audio.wav" 

def record_audio(file_path, duration=DURATION, sample_rate=SAMPLE_RATE):
    """Record audio from the microphone and save it as a WAV file."""
    print(f"Recording for {duration} seconds...")

    # Record audio
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()  # Wait until recording is complete

    # Save as WAV file
    wav.write(file_path, sample_rate, audio_data)
    print(f"Audio file saved: {file_path}")

def upload_audio(file_path):
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'audio/wav')}
            response = requests.post(SERVER_URL, files=files)
        
        # Display server response
        print("Server response:", response.status_code, response.json())
    
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    record_audio(FILE_PATH)  # Record voice input
    time.sleep(1) 
    upload_audio(FILE_PATH)  # Upload file to the server

import sounddevice as sd
import numpy as np
import torch
from transformers import pipeline
import time
import os
from datetime import datetime

# recording parameters
SAMPLE_RATE = 44100
CHANNELS = 1
RECORD_SECONDS = 5

# emotion analysis pipeline
emotion_analyzer = pipeline("text-classification", model="finiteautomata/bertweet-base-emotion-analysis")

def analyze_emotion(text):
    result = emotion_analyzer(text)
    return result[0]['label']

def record_audio():
    # record audio
    recording = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype='float32'
    )
    
    sd.wait()    
    return recording

def save_audio(recording):
    filename = f"temp_recording_{int(time.time())}.wav"
    
    # convert to 16-bit PCM
    recording = np.int16(recording * 32767)
    
    # save using soundfile
    import soundfile as sf
    sf.write(filename, recording, SAMPLE_RATE)
    
    return filename

def main():
    print("ML client container started. Ready to record and analyze emotions.")
    
    try:
        while True:
            recording = record_audio()
            audio_file = save_audio(recording)
            
            # TODO: add speech-to-text conversion here
            # for now, we'll use a placeholder text
            text = "Very very nice day"
            
            emotion = analyze_emotion(text)
            print(f"Detected emotion: {emotion}")
            
            # clean up temporary file
            os.remove(audio_file)
            
    except KeyboardInterrupt:
        print("\nStopping emotion analysis...")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()


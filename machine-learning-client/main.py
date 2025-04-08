import sounddevice as sd
import numpy as np
from transformers import pipeline
import time
import os
import speech_recognition as sr
import soundfile as sf

# recording parameters
SAMPLE_RATE = 44100
CHANNELS = 1
RECORD_SECONDS = 5

# initialize speech recognizer
recognizer = sr.Recognizer()
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
    filename = f"./machine-learning-client/temp_recording_{int(time.time())}.wav"
    
    # convert to 16-bit PCM
    recording = np.int16(recording * 32767)

    sf.write(filename, recording, SAMPLE_RATE)
    return filename

def speech_to_text(audio_file):
    # convert speech to text using google's speech recognition
    try:
        with sr.AudioFile(audio_file) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)
            
            # use google's speech recognition
            text = recognizer.recognize_google(audio_data)
            # print(f"Transcription: {text}")
            return text
            
    except sr.UnknownValueError:
        print("Google Speech Recognition couldn't understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
    except Exception as e:
        print(f"Error in speech recognition: {str(e)}")
        return None


def main():
    print("ML client container started. Ready to record and analyze emotions.")

    try:
        while True:
            recording = record_audio()
            audio_file = save_audio(recording)
       
            # convert speech to text
            text = speech_to_text(audio_file)
        
            # analyze emotion from text
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

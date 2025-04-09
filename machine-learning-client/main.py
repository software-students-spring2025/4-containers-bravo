"""Machine Learning Client for emotion analysis from speech.

This module provides functionality to record audio, convert speech to text,
and analyze emotions from the transcribed text using a pre-trained model.
"""

import os
import time
import requests
import numpy as np
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from transformers import pipeline

# recording parameters
SAMPLE_RATE = 44100
CHANNELS = 1
RECORD_SECONDS = 5

# initialize speech recognizer
recognizer = sr.Recognizer()
# emotion analysis pipeline
emotion_analyzer = pipeline(
    "text-classification", model="finiteautomata/bertweet-base-emotion-analysis"
)


def analyze_emotion(text):
    """Analyze emotion from given text using a pre-trained model.

    Args:
        text (str): Input text to analyze

    Returns:
        str: Detected emotion label
    """
    result = emotion_analyzer(text)
    return result[0]["label"]


def record_audio():
    """Record audio from the default input device.

    Returns:
        numpy.ndarray: Recorded audio data
    """
    recording = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32",
    )
    sd.wait()
    return recording


def save_audio(recording):
    """Save recorded audio to a temporary WAV file.

    Args:
        recording (numpy.ndarray): Audio data to save

    Returns:
        str: Path to the saved audio file
    """
    filename = f"./machine-learning-client/temp_recording_{int(time.time())}.wav"
    recording = np.int16(recording * 32767)
    sf.write(filename, recording, SAMPLE_RATE)
    return filename


def speech_to_text(audio_file):
    """Convert speech from audio file to text using Google's speech recognition.

    Args:
        audio_file (str): Path to the audio file

    Returns:
        str: Transcribed text or None if recognition fails
    """
    try:
        with sr.AudioFile(audio_file) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        print("Google Speech Recognition couldn't understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error in speech recognition: {str(e)}")
        return None

def send_emotion_request(emotion):
    """Send emotion to the server.

    Args:
        emotion (str): Emotion to send
    """
    try:
        response = requests.post(
            "http://0.0.0.0:5001/api/emotions",
            json={"emotion": emotion},
            timeout=5
        )
        if response.status_code == 200:
            print(f"Successfully sent emotion: {emotion}")
        else:
            print(f"Failed to send emotion. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending emotion to server: {str(e)}")


def main():
    """Main function to run the emotion analysis loop."""
    print("ML client container started. Ready to record and analyze emotions.")

    try:
        while True:
            recording = record_audio()
            audio_file = save_audio(recording)
            text = speech_to_text(audio_file)
            if text:
                emotion = analyze_emotion(text)
                print(f"Detected emotion: {emotion}")

                # send emotion to web app
                send_emotion_request(emotion)

            # remove audio file
            os.remove(audio_file)

    except KeyboardInterrupt:
        print("\nStopping emotion analysis...")
    except Exception as e:  # pylint: disable=broad-except
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()

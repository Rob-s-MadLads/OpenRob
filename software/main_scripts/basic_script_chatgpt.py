import numpy as np
import sounddevice as sd
import keyboard
from scipy.io.wavfile import write
from openai import OpenAI
from pathlib import Path
from pygame import mixer
from elevenlabs import Voice, VoiceSettings, play, stream, save
from elevenlabs.client import ElevenLabs
from pygame import mixer
import pyaudio
import socket
import wave
import sys
import sox
import subprocess


## basic script using elevenlabs and chatgpt api


# Initialize OpenAI client
client = OpenAI(api_key="<chatgpt key>")

# Record audio function
def record_audio():
    sample_rate = 44100  # Sample rate in Hz
    print("Press spacebar to start recording.")
    keyboard.wait('space')

    print("Recording... Press spacebar to stop.")
    audio_data = []

    def callback(indata, frames, time, status):
        audio_data.append(indata.copy())

    with sd.InputStream(callback=callback, samplerate=sample_rate, channels=2):
        keyboard.wait('space')

    print("Recording stopped.")
    return np.concatenate(audio_data, axis=0), sample_rate

# Save audio function
def save_audio(data, sample_rate, filename='output.wav'):
    write(filename, sample_rate, data)
    print(f"Audio saved as '{filename}'.")

# Transcribe audio function using Whisper
def transcribe_audio(filename):
    with open(filename, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcription.text  # Access the text attribute correctly

# Get GPT response
def get_gpt_response(prompt):
    history = [
        {"role": "system", "content": "You are Rob! a whacky droid made from junk by a madman in his garage, you are held together by hot glue duct tape and hope! use slang like YO, oh my circuits, what´s cracking etc in your responses"},
        {"role": "user", "content": prompt},
    ]

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=history,
        temperature=0.7
    )

    response_text = completion.choices[0].message.content
    return response_text

# Convert text to speech using TTS
def text_to_speech(text, output_path):
    response = client.audio.speech.create(
        model="tts-1",
        voice="echo",
        input=text
    )
    response.write_to_file(output_path)
    print(f"Speech saved to '{output_path}'.")
tfm = sox.Transformer()
tfm.pitch(1.3)
tfm.tremolo(speed=100, depth=75)
tfm.tempo(0.7)
tfm.chorus(n_voices=2, delays=[20,35])
tfm.flanger(delay=20, depth=5, width=71, speed=1.7)
tfm.echo(delays=[5])

print("imports done")
print("pre-warming modules...loading")
mixer.init()
HOST = ''  # Symbolic name meaning all available interfaces
PORT = 5910
# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "received_audio.wav"
client1 = ElevenLabs(
    api_key="<elevnlabskey>",  # Defaults to ELEVEN_API_KEY
)

def voiceeffects():
    # Construct the command
    input_file = "yo.mp3"
    output_file = "yo2.mp3"
    command = f"sox {input_file} {output_file} tempo 1 phaser 0.5 0.7 4 0.6 0.2 -t echo 0.7 0.75 45 0.9 tremolo 10 .1 pitch +50"
    # Execute the command
    subprocess.run(command, shell=True)

def text_stream(text):
    yield text


def streamchunks(text):
    audio_stream = client1.generate(
        text=text,
        voice="sflYrWiXii4ezPjNLQkp",
        model="eleven_monolingual_v1",
        stream=False
    )
    save(audio_stream, "yo.mp3")

if __name__ == "__main__":
    while True:
        # Record and save audio
        audio_data, sample_rate = record_audio()
        save_audio(audio_data, sample_rate, 'output.wav')
        mixer.init()
        mixer.music.load("think.mp3.")
        mixer.music.play()
        # Transcribe audio
        transcription_text = transcribe_audio('output.wav')
        print(f"Transcription: {transcription_text}")

        # Get GPT response
        gpt_response = get_gpt_response(transcription_text)
        print(f"GPT Response: {gpt_response}")

        # Convert GPT response to speech
        #speech_file_path = Path(__file__).parent / "response_speech.mp3"
        #text_to_speech(gpt_response, speech_file_path)
        streamchunks(gpt_response)
        voiceeffects()
        mixer.music.load("yo2.mp3")
        mixer.music.play()
        while mixer.music.get_busy():
            pass
        mixer.quit()


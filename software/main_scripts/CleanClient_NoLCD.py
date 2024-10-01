# Rob2.0 client script without LCD functions



import time
import RPi.GPIO as GPIO
print("importing")
import pyaudio
import socket
import sys
from time import sleep
from pygame import mixer
mixer.init()
import busio
import board
from gpiozero import CPUTemperature
import psutil
from vosk import Model, KaldiRecognizer
import json
from PIL import Image
import threading
import asyncio
from threading import Thread
from gpiozero import Button
import socket
import sys
from time import sleep

print("import done")

# Set up the GPIO pin for the button
button_pin = 26  # You can change this to the GPIO pin you're using

# Set up the GPIO library to use the BCM pin numbering
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set pin as input with internal pull-up resistor


def buttonpress():
    print("awaiting button")
    try:
        while True:
            # Read the button state
            button_state = GPIO.input(button_pin)

            if button_state == GPIO.HIGH:
                print("Button Pressed")
                break

            time.sleep(0.1)  # Small delay to debounce the button

    finally:
        print("exit button")




## audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024







def play_audio(audio):
    mixer.init()
    mixer.music.load(audio)
    mixer.music.play()
    while mixer.music.get_busy():
        pass




# input_file = 'audio2.mp3'
# output_file = 'file.wav'
def accept_connections(sock):
    conn, addr = sock.accept()
    print(f'Connected with mainframe ')
    sleep(1)
    return conn


def mainframe_connect():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Get local machine name
    host = "<host ip adress>""
    port = < host
    port >
    # Connection to hostname on the port.
    client_socket.connect((host, port))
    # Send a message
    message = "Rob! connected to mainframe!"
    client_socket.send(message.encode('ascii'))
    print("connected")
    
    # turn_on_color(green_pin)
    client_socket.close()




def receive_and_play_files(sock):
    
    filename = "audio12.mp3"
    while True:
        print("waiting for file")
        conn = accept_connections(sock)
        with conn:
            with open(filename, 'wb') as file:
                while True:
                    data = conn.recv(1024)
                    if data == b'done':
                        # mixer.music.pause()
                        print("Done signal received. Exiting...")
                        return  # Return to close the socket outside this function
                    if not data:
                        break  # End of file
                    file.write(data)
            
            play_audio("audio12.mp3") #audio file from server
            print("Waiting for next file...")
  

RPORT = < RPi
port
here >


def setup_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", RPORT))
    sock.listen(1)
    return sock


def get_cpu_usage():
    return psutil.cpu_percent()


def get_ram_usage():
    ram = psutil.virtual_memory()
    return ram.percent


def mainframe_data():
    cpu = CPUTemperature()
    cpu_usage = get_cpu_usage()
    ram_usage = get_ram_usage()
    current_time = time.strftime("%H:%M", time.localtime())
    CPU_VOLT_TEXT = f"[SYSTEM INFO]:\n[Time: {current_time}]\n[CPU usage: {cpu_usage}%]\n[RAM usage: {ram_usage}%]\n[CPU-Temp: {cpu.temperature:.2f}]\n\n"
    print(CPU_VOLT_TEXT)
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Get local machine name
    host = "<host ip>
    port = < yo mommas fat ass port here bitch >
    # Connection to hostname on the port.
    client_socket.connect((host, port))
    # Send a message
    client_socket.send(CPU_VOLT_TEXT.encode('ascii'))
    print("connected")
    # turn_on_color(green_pin)
    client_socket.close()


def stream_audio():
    mainframe_data()
    mixer.music.pause()
   
    buttonpress()
    sleep(1)
    audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("connecting")
    try:
        # Create a socket connection for sending data
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("host", GUESS))

    except Exception as e:
        print("connection error")

    try:
        
        while True:
            data = stream.read(CHUNK)
            client_socket.sendall(data)
            # usrinputs2=input(":")
            if GPIO.input(26):
                print('Touch Detected!')
                #       head_up()
                break
        # eyes_load()
    except KeyboardInterrupt:
        mixer.music.load("think.wav")
        mixer.music.play()
        print("stopping")
        pass

    # Stop and close the stream and socket
    stream.stop_stream()
    stream.close()
    audio.terminate()
    client_socket.close()


def main():
    while True:
        try:
            mainframe_connect()
            break
        except Exception as e:
            
            time.sleep(3)
            exit()
    sock = setup_socket()
    while True:
        receive_and_play_files(sock)
        stream_audio()


# mainframe_connect()

buttonpress()
main() 

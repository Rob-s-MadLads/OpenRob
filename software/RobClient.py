# Rob2.0 Script adapted for LCD screen and what not

##LCD setup
import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd
import time
import RPi.GPIO as GPIO

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


# LCD Configuration
lcd_columns = 8
lcd_rows = 2
lcd_rs = digitalio.DigitalInOut(board.D25)
lcd_en = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D23)
lcd_d5 = digitalio.DigitalInOut(board.D17)
lcd_d6 = digitalio.DigitalInOut(board.D18)
lcd_d7 = digitalio.DigitalInOut(board.D22)

lcd = character_lcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
    lcd_columns, lcd_rows)


def LCDprint(message):
    lcd.clear()
    try:
        lcd.message = message
    except Exception as e:
        lcd.message = "  LCD\n ERROR"
        print(e)
        exit()


LCDprint("loading\n imports")
print("importing")
import pyaudio
import socket
import sys
from time import sleep
from pygame import mixer

mixer.init()
import sox
import busio
from adafruit_ina219 import INA219
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

## audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# import Eyes_idle_loop
print("import done")
import random


def cleareyes():
    lcd.clear()


cleareyes()
LCDprint("imports\ndone")

# Initialize the transformer
tfm = sox.Transformer()
tfm.pitch(1.3)
tfm.tremolo(speed=100, depth=75)
tfm.tempo(0.7)
tfm.chorus(n_voices=2, delays=[20, 35])
tfm.flanger(delay=20, depth=5, width=71, speed=1.7)
tfm.echo(delays=[5])


def play_audio(audio):
    mixer.init()
    mixer.music.load(audio)
    mixer.music.play()
    while mixer.music.get_busy():
        pass


def voiceffects(voice):
    input_file = voice
    output_file = 'voiceeffects.wav'
    tfm.build_file(input_file, output_file)


# input_file = 'audio2.mp3'
# output_file = 'file.wav'
def accept_connections(sock):
    conn, addr = sock.accept()
    print(f'Connected with mainframe ')
    sleep(1)
    return conn


def mainframe_connect():
    LCDprint("connecting to server")
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
    cleareyes()
    LCDprint("server\nresponded")

    # turn_on_color(green_pin)
    client_socket.close()


import socket
import sys
from time import sleep


def receive_and_play_files(sock):
    # head_down()
    # think()
    # eyes_load()
    # turn_on_color(blue_pin)
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
            # head_mid()
            #             eyes = [eyes_right, eyes_left, eyes_still]
            #             random_eyes = random.choice(eyes)
            #             random_eyes()
            # tfm.build_file(filename, "audio12.mp3")
            # head_up()
            #             turn_on_color(blue_pin)
            play_audio("audio12.mp3")
            print("Waiting for next file...")
    # head_mid()


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
    LCDprint("press\button")
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
        LCDprint(" recording\n now")
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
            LCDprint("error\n in main")
            time.sleep(3)
            LCDprint("exiting\nscript")
            exit()
    sock = setup_socket()
    while True:
        receive_and_play_files(sock)
        stream_audio()


# mainframe_connect()
lcd.clear()
LCDprint("press\nbutton")
# buttonpress()
main()
# LCDprint(" RobOS\n  4.0")














## Rob3.0
import subprocess
print("importing")
import time
import asyncio
import pyaudio
import socket
import sys
from time import sleep
from pygame import mixer
mixer.init()
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
import lgpio
import wave
import cv2
import asyncio
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image
import os


print("import done")


# Define the button
button = Button(12, pull_up=True)  # GPIO 16, using internal pull-up resistor

# def ButtonPress():
#     print("Waiting for button press...")
#     button.wait_for_press()  # Blocks until the button is pressed
#     print("Button was pressed!")
#     return

def ButtonPress():
    print("Waiting for button press...")
    while True:
        try:
            print("interupt with keyboard")
            sleep(0.5)
        except KeyboardInterrupt:
            break
    #button.wait_for_press()  # Blocks until the button is pressed
    print("keyboard was pressed!")
    return



## audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024





# Constants
HEAD1 = 21  # GPIO pin for PWM
PWM_FREQ = 50  # Frequency in Hz

def HeadUp():
    handle = lgpio.gpiochip_open(0)  # Open the GPIO chip
    lgpio.gpio_claim_output(handle, HEAD1)  # Set the pin as output
       
    lgpio.tx_pwm(handle, HEAD1, PWM_FREQ, 0)  # Move servo to desired position
    sleep(0.5)
    
    lgpio.tx_pwm(handle, HEAD1, PWM_FREQ, 6)  # Move servo to desired position
    sleep(0.5)

    lgpio.tx_pwm(handle, HEAD1, PWM_FREQ, 0)  # Stop PWM (duty cycle 0)
    lgpio.gpiochip_close(handle)  # Close the GPIO chip

def HeadMid():
    handle = lgpio.gpiochip_open(0)  # Open the GPIO chip
    lgpio.gpio_claim_output(handle, HEAD1)  # Set the pin as output

    
    lgpio.tx_pwm(handle, HEAD1, PWM_FREQ, 0)  # Move servo to desired position
    sleep(0.5)


    lgpio.tx_pwm(handle, HEAD1, PWM_FREQ, 7.5)  # Move servo to desired position
    sleep(0.5)

    lgpio.tx_pwm(handle, HEAD1, PWM_FREQ, 0)  # Stop PWM (duty cycle 0)
    lgpio.gpiochip_close(handle)  # Close the GPIO chip
def HeadDown():
    handle = lgpio.gpiochip_open(0)  # Open the GPIO chip
    lgpio.gpio_claim_output(handle, HEAD1)  # Set the pin as output

    lgpio.tx_pwm(handle, HEAD1, PWM_FREQ, 0)  # Move servo to desired position
    sleep(0.5)


    lgpio.tx_pwm(handle, HEAD1, PWM_FREQ, 9.9)  # Move servo to desired position
    sleep(0.5)

    lgpio.tx_pwm(handle, HEAD1, PWM_FREQ, 0)  # Stop PWM (duty cycle 0)
    lgpio.gpiochip_close(handle)  # Close the GPIO chip
   


def play_audio(audio):
    mixer.init()
    mixer.music.load(audio)
    send_command("EyesLeft")
    mixer.music.play()
    while mixer.music.get_busy():
        pass


def accept_connections(sock):
    conn, addr = sock.accept()
    print(f'Connected with mainframe ')
    return conn  # Successful connection, return it


def MainframeCommand(message):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Get local machine name
    host = "192.168.194.135"
    port = 42069   # Connection to hostname on the port.
    client_socket.connect((host, port))
    # Send a message
    message = f"{message}"
    client_socket.send(message.encode('ascii'))
    print(f"sending command: {message}")
    
    # turn_on_color(green_pin)
    client_socket.close()

def mainframe_connect():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Get local machine name
    host = "192.168.194.135"
    port = 42069   # Connection to hostname on the port.
    client_socket.connect((host, port))
    # Send a message
    message = "Rob! connected to mainframe!"
    client_socket.send(message.encode('ascii'))
    print(message)
    
    # turn_on_color(green_pin)
    client_socket.close()

def receive_and_play_files(sock):
    HeadDown()
    conn = accept_connections(sock)
    with conn:
        while True:
            try:
                # Read header
                header = conn.recv(4)
                if not header:
                    break
                file_size = int.from_bytes(header, byteorder='big')
                
                if file_size == 0:  # Termination signal
                    print("Stream ended")
                    break
                
                # Read audio data
                received_data = b''
                while len(received_data) < file_size:
                    chunk = conn.recv(min(4096, file_size - len(received_data)))
                    if not chunk:
                        break
                    received_data += chunk
                
                # Play audio in a thread to avoid blocking
                #threading.Thread(target=play_audio, args=(received_data,)).start()
                send_command("EyesTalk")
                HeadMid()
                play_audio_temp(received_data)
            except socket.timeout:
                print("Timeout waiting for data")
                break

def play_audio_temp(data):
    temp_file = f"temp_{time.time()}.wav"
    with open(temp_file, 'wb') as f:
        f.write(data)
    mixer.music.load(temp_file)
    mixer.music.play()
    while mixer.music.get_busy():
        pass
    HeadDown()
    os.remove(temp_file)
    send_command("EyesLoading")
    Think()



# 
# def receive_and_play_file():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     sock.bind(("", 42068))
#     sock.listen(1)
#     print("Waiting for connection...")
# 
#     conn, addr = sock.accept()
#     print(f"Connected with {addr}")
# 
#     filename = "audio12.wav"
#     with conn, open(filename, 'wb') as file:
#         print("Receiving file...")
#         while True:
#             data = conn.recv(1024)
#             if not data or data == b'done':  # Stop receiving when 'done' signal arrives
#                 break
#             file.write(data)
# 
#     print("File received successfully.")
#     conn.close()
#     sock.close()
#     print("Rob is talking")
#     send_command("EyesTalk")
#     HeadMid()
#     play_audio("audio12.wav") #audio file from server
#     sleep(1)
#     print("Rob is thinking...")
#     send_command("EyesIdle")
#     HeadMid()






RPORT = 42068

port = ""
here = ""


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

def mainframe_prompt(prompt):
      # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Get local machine name
    host = "192.168.194.135"
    port = 42069
    # Connection to hostname on the port.
    client_socket.connect((host, port))
    # Send a message
    client_socket.send(prompt.encode('ascii'))
    print("data sent")
    # turn_on_color(green_pin)
    client_socket.close()

def mainframe_data():
    cpu = CPUTemperature()
    cpu_usage = get_cpu_usage()
    ram_usage = get_ram_usage()
    current_time = time.strftime("%H:%M", time.localtime())
    battery_level = "N/A"
    CPU_VOLT_TEXT = f"[SYSTEM INFO]:\n[Time: {current_time}]\n[CPU usage: {cpu_usage}%]\n[RAM usage: {ram_usage}%]\n[CPU-Temp: {cpu.temperature:.2f}]\n[BATTERY: {battery_level}]\n"
    print(CPU_VOLT_TEXT)
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Get local machine name
    host = "192.168.194.135"
    port = 42069
    # Connection to hostname on the port.
    client_socket.connect((host, port))
    # Send a message
    client_socket.send(CPU_VOLT_TEXT.encode('ascii'))
    print("data sent")
    # turn_on_color(green_pin)
    client_socket.close()


def mainframe_omegle():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Get local machine name
    host = "192.168.194.135"
    port = 42069
    # Connection to hostname on the port.
    client_socket.connect((host, port))
    # Send a message
    client_socket.send("you connected with a person on a chat roulette/omegle type website say hi".encode('ascii'))
    print("tick sent")
    # turn_on_color(green_pin)
    client_socket.close()

def stream_audio():
    mainframe_data()
    mixer.music.pause()
    ButtonPress()
    sleep(1)
    HeadMid()
    audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("connecting")
    try:
        # Create a socket connection for sending data
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("192.168.194.135", 42069))

    except Exception as e:
        print("connection error")

    try:
        print("streaming")
        while not Button.is_pressed:
            data = stream.read(CHUNK)
            client_socket.sendall(data)
                
                
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


def SendVoice(file_path):
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect(("192.168.194.135", 42069))
        print(f"Connected to server")
        
        # Open the file and send its content
        with open(file_path, "rb") as file:
            while chunk := file.read(4096):
                client_socket.sendall(chunk)
        
        print("File sent successfully.")
        



def RecordMic():
    try:
        HeadDown()
        print("press button to talk")
        send_command("EyesLeft")
        mixer.music.stop()
        ButtonPress()
        #button.wait_for_press()
        sleep(0.5)
        HeadMid()
        frames = []
        filename = "VoiceRecord.wav"
        chunk = 1024
        FORMAT = pyaudio.paInt16
        channels = 1
        sample_rate = 44100
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        output=True,
                        frames_per_buffer=chunk)

        print("recording started")
        send_command("EyesLeft")
        #while not button.is_pressed:
#         while button.is_pressed:
#             data = stream.read(chunk)
#             frames.append(data)
        while not button.is_pressed:
            try:
                data = stream.read(chunk)
                frames.append(data)
            except KeyboardInterrupt:
                break
        send_command("EyesLoading")
        HeadDown()
        send_command("EyesLoading")
        #send_command("EyesLeft")
        print("recording stopped")
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(filename, "wb")
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))
        wf.close()
    except KeyboardInterrupt:
        exit()

def RecordMicOmegle():
    try:
        HeadMid()
        print("press button to talk")
        send_command("EyesWait")
        mixer.music.stop()
        button.wait_for_press()
        HeadMid()
        frames = []
        filename = "VoiceRecord.wav"
        chunk = 1024
        FORMAT = pyaudio.paInt16
        channels = 1
        sample_rate = 44100
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        output=True,
                        frames_per_buffer=chunk)

        print("recording started")
        send_command("TalkNow")
        while button.is_pressed:
            data = stream.read(chunk)
            frames.append(data)
        send_command("EyesLoading")
        HeadDown()
        send_command("EyesLoading")
        #send_command("EyesLeft")
        print("recording stopped")
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(filename, "wb")
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))
        wf.close()
    except KeyboardInterrupt:
            OmegleYo()
            RecordMic()


            
def ReceiveCommand(sock):
        while True:
            conn = accept_connections(sock)
            with conn:
                while True:
                    command = conn.recv(1024)
                    if not command:
                        break
                    print("Received command:", command.decode())
                    break
            conn.close()
                    
                

def ReceiveVoice():
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind to the specified address and port
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("", 42068))
        print(f"Server is listening for audio...")

        # Listen for incoming connections
        server_socket.listen(1)
        conn, addr = server_socket.accept()

        print(f"Connected by {addr}")
        with conn:
            # Open file to write incoming data
            with open("audio12.wav", "wb") as file:
                while True:
                    data = conn.recv(4096)
                    if data == b'done':
                        # mixer.music.pause()
                        print("Done signal received. Exiting...")
                        return  # Return to close the socket outside this function

                    if not data:  # End of data
                        break
                    file.write(data)







def Think():
    send_command("EyesLoading")
    mixer.music.set_volume(1)
    mixer.music.load("think.wav")
    mixer.music.play()


def main():
    HeadDown()
    send_command("EyesLoading")
    while True:
        try:
            mainframe_connect()
            sleep(3)
            mainframe_data()
            sleep(3)
            MainframeCommand("llm")
            sleep(1)
            break
        except Exception as e:
            print(e)
            time.sleep(3)
            exit()
    sock = setup_socket()
    while True:
        sleep(1)
        Think()
        receive_and_play_files(sock)
        sleep(1)
        HeadDown()
        RecordMic()
        Think()
        sleep(1)
        SendVoice("VoiceRecord.wav")
        sleep(1)


def pingtest():
    try:
       subprocess.check_call(["ping","-c" "1", "192.168.194.135"])
    except Exception as e:
        print(f"error: \n {e}")  
    finally:
        print("response recieved")

    

def send_command(command):
    with open("eye_command.txt", "w") as file:
        file.write(command)
def OsBoot():
    mixer.music.load("OsBoot.mp3")
    mixer.music.play()

def RecordMic2(record_seconds=5):
    HeadMid()
    print(f"Recording will start for {record_seconds} seconds...")
    HeadMid()
    send_command("TalkNow")
    
    frames = []
    filename = "VoiceRecord.wav"
    chunk = 1024
    FORMAT = pyaudio.paInt16
    channels = 1
    sample_rate = 44100
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)

    print("Recording started...")
    start_time = time.time()
    while time.time() - start_time < record_seconds:
        data = stream.read(chunk)
        frames.append(data)

    HeadMid()
    print("Recording stopped")
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio
    with open(filename, "wb") as f:
        f.write(b''.join(frames))
    print(f"Recording saved as {filename}")


def mainTest():
    HeadDown()
    send_command("EyesLoading")
    while True:
        try:
            mainframe_connect()
            sleep(3)
            mainframe_prompt()
            sleep(3)
            MainframeCommand("llm")
            sleep(1)
            break
        except Exception as e:
            print(e)
            time.sleep(3)
            exit()

    while True:
        sleep(1)
        Think()
        receive_and_play_files()
        sleep(1)
        HeadDown()
        RecordMic()
        send_command("EyesLoading")
        SendVoice("VoiceRecord.wav")
            

#RecordMic2()
#OmegleYo()
# send_command("EyesLeft")
# HeadMid()
#ButtonPress()
# Example commands:
# pingtest()
# Think()
# stream_audio()
#OsBoot()
#send_command("StartUp")

def OmegleYo():
    try:
        input(":")
        HeadMid()
        #send_command("EyesLeft")
        play_audio("Yo!.wav")
    except KeyboardInterrupt:
        print("going to SendVoice")
        
def OmegleMain():
    while True:
        try:
            HeadDown()
            mainframe_connect()
            sleep(3)
            mainframe_prompt("starting omegle function")
            sleep(3)
            MainframeCommand("Omegle")
            sleep(1)
            break
        except Exception as e:
            print(e)
            time.sleep(3)
    sock = setup_socket()
    while True:
        OmegleYo()
        send_command("EyesWait")
        RecordMicOmegle()
        HeadDown()
        send_command("EyesLoading")
        SendVoice("VoiceRecord.wav")
        HeadMid()
        receive_and_play_files(sock)
        
# while True:
#     send_command("EyesLeft")
#     HeadMid()
#     HeadDown()
#     send_command("EyesRight")


ButtonPress()

inputs = input(":")
# import BootVideo
# sleep(5)
if "omegle" in inputs:
    OmegleMain()
if "main" in inputs:
    main()
else:
    exit()


# mainframe_connect()
# sock = setup_socket()
# receive_and_play_files(sock)

# main() 



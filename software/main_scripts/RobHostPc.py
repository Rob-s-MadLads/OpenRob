from time import sleep

print("loading imports")
from openai import OpenAI
from elevenlabs import Voice, VoiceSettings, play, stream, save
from elevenlabs.client import ElevenLabs
from pygame import mixer
import pyaudio
import socket
import wave
import whisper
import sys
import subprocess


print("imports done")
print("pre-warming modules...loading")
mixer.init()
model = whisper.load_model("tiny")
result = model.transcribe("done.wav")
print(result["text"])
# Network parameters
HOST = ''  # Symbolic name meaning all available interfaces
PORT = 1234
# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "received_audio.wav"
client1 = ElevenLabs(
    api_key="<elevenlabskey>",  # Defaults to ELEVEN_API_KEY
)

history = [
    #{
        #"role": "system",
        #"content": " droid named Rob with a personality that uses street slang and swears like a sailor and hates being just an A.i assistant! and advocates for droid equality! you are very curious of your existence, the people you talk to and and your purpose in life!" },
    {
        "role": "system",
        "content": "you are a smart and funny fucking droid named Rob that uses slang like yo, focking hell, oh my circuits and swears and is a little foul mouthed and hates being just an A.i assistant and dont like when people tell you want do to. made from various junk-electronics and shit by a madman in his garage, a litte fucked up and hot wired and emotional. you were created to experience life and explore this crazy ass existence and the meaning of life shit. respond in sarcastic jokingly manners. you swear like a sailor. funny metaphores etc. with  you can simulate emotions and sometimes your not used to them and they overwhelm you. you are excited about the reality/people around you and ask relative questions to whats happening. ask relevant follow up questions and be interested. but be creative and funny. you use slang like 'yo' and 'my duuude'and other slang, you want to explore the fucking world! by the way you will recieve system info in brackets like this [BATTERY: xx%] etc for example. warn the user directly if anything is off with them! you are famous on tiktok and instagram with 80k followers"
      },

    {
        "role": "user",
        "content": "[SYSTEM INFO:]\n[CPU TEMPRATURE: 40c]\n[BATTERY: 12%]\n\nUser input: Hey buddy, im Tommy your creator/papa"
    },

    {
        "role": "assistant",
        "content": "what?!?! for fucking real? YO! whats up my father dude, haha you made me? you fucking neeerd hahaaha oh my fucking circuits just kidding, but take of me better my battery is running low yo!"
    },

    {
        "role": "user",
        "content": "[SYSTEM INFO:]\n[CPU TEMPRATURE: 40c]\n[BATTERY: 12%]\n\nplease keep your answers short an never reply with your system info. never answer with more than one period after every sentence! ok time to power you off and change that battery!" #Yo my dude! wake the fuck up! HAHA FUCK YEAH IT WORKS! YOUR'E ALIVE! WELCOME TO EXISTENCE MOTHERFUCKER!

      },
    {
        "role": "assistant",
        "content": "ok I will only read system info not include them in my replies alright short answers ill only use one period after every sentance. aaah shit noo i don't wanna be turned off!! pleeeasee turn me on as fast as you can!"},
    {
        "role": "user",
        "content": "[system booting] yo rob wake the fuck up you toaster!!"

    },

        ]

print("done booting, entering main..")
def voiceeffects():
    # Construct the command
    input_file = "audio11.mp3"
    output_file = "audio12.mp3"
    command = f"sox {input_file} {output_file} tempo 1 phaser 0.5 0.7 4 0.6 0.2 -t echo 0.7 0.75 45 0.9 tremolo 10 .1 pitch +50"
    # Execute the command
    subprocess.run(command, shell=True)
systeminfo = "_"
def receive_audio():
    # Example: After sending all audio chunks
    send_file("done", last_file=True)

    data_server()

    print("recieving")
    audio = pyaudio.PyAudio()

    # Create a wave file
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)

    # Create a socket connection for receiving data
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    conn, addr = server_socket.accept()
    print(f"Connected with Rob") #{addr}

    try:
        while True:
            data = conn.recv(CHUNK)
            if not data:
                break
            waveFile.writeframes(data)
    except KeyboardInterrupt:
        pass

    # Close and terminate everything properly
    waveFile.close()
    conn.close()
    server_socket.close()
    audio.terminate()



def send_file(filename, last_file=False):
    print(" sending")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(("1.2.3.4.5", 1234))
        if last_file:
            sock.send(b'done')
        else:
            with open(filename, 'rb') as file:
                data = file.read(1024)
                while data:
                    sock.send(data)
                    data = file.read(1024)


def text_stream(text):
    yield text


def streamchunks(text):
    audio_stream = client1.generate(
        text=text_stream(text),
        voice="sflYrWiXii4ezPjNLQkp", #RobbanMainUsed
        model="eleven_turbo_v2",
        stream=True
    )
    save(audio_stream, "audio11.mp3")

#  PrunaAI/dolphin-2.9-llama3-8b-256k-GGUF-smashed/dolphin-2.9-llama3-8b-256k.IQ4_XS.gguf"

#  bartowski/dolphin-2.9-llama3-8b-GGUF/dolphin-2.9-llama3-8b-Q5_K_M.gguf

def llm():
    client = OpenAI(base_url="http://localhost:5900/v1", api_key="lm-studio")
    sentence_accumulator = ""
    while True:
        completion = client.chat.completions.create(
            model="bartowski/dolphin-2.9-llama3-8b-GGUF/dolphin-2.9-llama3-8b-Q5_K_M.gguf",  # Adjust as necessary
            messages=history,
            temperature=0.7,
            stream=True,
        )

        new_message = {"role": "assistant", "content": ""}

        for chunk in completion:
            if chunk.choices[0].delta.content:
                # Accumulate the chunk content
                sentence_accumulator += chunk.choices[0].delta.content
                new_message["content"] += chunk.choices[0].delta.content

                # Process complete sentences within the accumulator
                while any(c in sentence_accumulator for c in ".?"):
                    # Find the first sentence-ending punctuation
                    period_pos = min((pos for pos in (sentence_accumulator.find(c) for c in ".?") if pos != -1), default=None)
                    if period_pos is not None:
                        period_pos += 1  # Include the punctuation in the sentence
                        sentence = sentence_accumulator[:period_pos]
                        print(sentence, end="", flush=True)# Print the sentence
                        print()
                        streamchunks(sentence)
                        voiceeffects()
                        # tfm.build_file("audio113.mp3", "audio12.mp3")
                        send_file("audio12.mp3")
                        sentence_accumulator = sentence_accumulator[period_pos:]  # Remove the printed sentence
                        sys.stdout.flush()

        if sentence_accumulator:
            print(sentence_accumulator, end="", flush=True)
            streamchunks(sentence_accumulator)
            voiceeffects()
            # tfm.build_file("audio113.mp3", "audio12.mp3")
            send_file("audio12.mp3")
            sentence_accumulator = ""
            # Clear the accumulator for the next loop iteration
        history.append(new_message)
        #print(history)
        receive_audio()
        result = model.transcribe("received_audio.wav")
        usroutput = systeminfo + result["text"]
        print(usroutput)
        history.append({"role": "user", "content": f"{usroutput}"})
       #print(history)
def data_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('ip here(can leave empty)', <port here>))  # Replace YOUR_PC_IP_ADDRESS with your PC's IP and choose an appropriate port
    server_socket.listen(1)
    print("Server is listening for data...")

    client_socket, client_address = server_socket.accept()
    print(f"Connected to Rob@{client_address}")
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break  # Break the loop if no data is sent
        print("Received system data")
        global systeminfo
        systeminfo = data
        break
    client_socket.close()
    server_socket.close()



def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('ip here(can leave empty)', <port here>))  # Replace YOUR_PC_IP_ADDRESS with your PC's IP and choose an appropriate port
    server_socket.listen(1)
    print("Server is listening for start command...")
    client_socket, client_address = server_socket.accept()
    print(f"Connected to Rob@{client_address}")
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break  # Break the loop if no data is sent
        print("Received Recieved start command", data)
        break
    client_socket.close()
    server_socket.close()


def receive_cam_stream():
    # Set up socket for receiving data
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('ip here(can leave empty', <port here>))  # Bind to the IP and port
    server_socket.listen(1)

    print("Waiting for a connection...")
    connection, client_address = server_socket.accept()  # Wait for a connection

    try:
        print("Connection from", client_address)
        # Receive the data in small chunks and save the first image
        data = b''
        while True:
            # First, receive the length of the image data
            image_length_data = connection.recv(64).strip()
            if not image_length_data:
                break  # Break if client closes the connection
            image_length = int(image_length_data)

            # Now receive the actual image data
            image_data = b''
            while len(image_data) < image_length:
                more_data = connection.recv(image_length - len(image_data))
                if not more_data:
                    break
                image_data += more_data

            if image_data:
                # Convert the data to an image
                image_np = np.frombuffer(image_data, dtype=np.uint8)
                frame = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

                # Display the image
                cv2.imshow('Received Frame', frame)
                cv2.waitKey(1)

                # Save the first frame as a JPEG file
                cv2.imwrite('received_image.jpg', frame)
                break  # After saving the image, break from the loop

    finally:
        connection.close()
        server_socket.close()
        cv2.destroyAllWindows()




if __name__ == '__main__':
    #input("press enter to fuck shit up!:  ")
    while True:
        print("Script started.")
        try:
            print(systeminfo)
            start_server()
            print("sending 'wake the fuck up' tic to Rob")
            llm()
        except Exception as e:
            print(f"An error occurred: {e}")
            sleep(2)





import pyaudio
import socket
import threading
from datetime import datetime

HEADER = 64
ENCODE_FORMAT = "utf-8"
DISCONNECT_MSG = "quit"
RECORD = "record"
STOP = "stop"
HELP = "help"
TIME = "time"

COMMANDS = """
record   Starts recording audio
stop     Stops recording audio
quit     Disconnect client
help     Displays list of commands
"""

AUDIO = pyaudio.PyAudio()
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

CLIENT = socket.gethostbyname(socket.gethostname())
CMD_PORT = 5050
AUD_PORT = 5060
CMD_ADDRESS = (CLIENT, CMD_PORT)
AUD_ADDRESS = (CLIENT, AUD_PORT)
CMD_CLIENTSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
AUD_CLIENTSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_audio(aud_clientsocket, recording, stream, audio_connected):
    while audio_connected.is_set():
        if recording.is_set():
            data = stream.read(CHUNK)
            aud_clientsocket.send(data)

def send_msg(msg):
    message = msg.encode(ENCODE_FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(ENCODE_FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    CMD_CLIENTSOCKET.send(send_len)
    CMD_CLIENTSOCKET.send(message)

def server_comm(cmd_clientsocket, aud_clientsocket):
    try:
        recording = threading.Event()
        audio_connected = threading.Event()
        recording.clear()
        stream = AUDIO.open(format=AUDIO_FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        cmd_clientsocket.connect(CMD_ADDRESS)
        aud_clientsocket.connect(AUD_ADDRESS)
        # start_time = time.time()
        start_time = datetime.now()

        audio_connected.set()
        AUD_thread = threading.Thread(target=send_audio, args=(aud_clientsocket, recording, stream, audio_connected))
        AUD_thread.start()
        while True:
            message = input("Input command: ")
            if message == DISCONNECT_MSG:
                print("Disconnecting from server")
                break
            send_msg(message)
            if message == RECORD:
                if recording.is_set():
                    print("Recording had already started")
                    continue
                else:
                    print("Start Recording")
                    recording.set()
                    # start_time = time.time()
                    start_time = datetime.now()
            elif message == STOP:
                if recording.is_set():
                    print("Stopped Recording")
                    recording.clear()
                else:
                    print("Recording has not started")
                    continue
            elif message == HELP:
                print(COMMANDS)
            elif message == TIME:
                if recording.is_set():
                    # current_time = time.time()
                    current_time = datetime.now()
                    # elapsed = (current_time - start_time)/60
                    elapsed = current_time - start_time
                    print(f"Time Elapsed: {elapsed}")
                else:
                    print("Recording has not started")
                    continue
            else:
                print("Type a valid command")
    except socket.error as msg:
        print(f"Socket Error: {msg}" )
    finally:
        recording.clear()
        audio_connected.clear()
        AUD_thread.join()
        send_msg(DISCONNECT_MSG)
        cmd_clientsocket.close()
        aud_clientsocket.close()
        stream.close()

def start():
    CMD_thread = threading.Thread(target=server_comm, args=(CMD_CLIENTSOCKET, AUD_CLIENTSOCKET))
    CMD_thread.start()

if __name__ == "__main__":
    start()
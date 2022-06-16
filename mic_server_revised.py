import pyaudio
import socket
import threading
import shutil
import wave
import datetime
# import transcribe

HEADER = 64
DECODE_FORMAT = "utf-8"
DISCONNECT_MSG = "quit"
RECORD = "record"
STOP = "stop"

AUDIO = pyaudio.PyAudio()
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# WAVE_OUTPUT_FILENAME = "output"
FILE_EXTENSION = ".wav"
BASE_PATH = "C:/Users/frost/OneDrive/Documents/audiorecorder/auto-note-taker/"
TRANSCRIBE_PATH = "C:/Users/frost/OneDrive/Documents/audiorecorder/Transcribe_Path/"

SERVER = socket.gethostbyname(socket.gethostname())
CMD_PORT = 5050
AUD_PORT = 5060
CMD_ADDRESS = (SERVER, CMD_PORT)
AUD_ADDRESS = (SERVER, AUD_PORT)
CMD_SERVERSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CMD_SERVERSOCKET.bind(CMD_ADDRESS)
AUD_SERVERSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
AUD_SERVERSOCKET.bind(AUD_ADDRESS)
 
def create_wavfile(frames):
    # file_number = len(os.listdir(TRANSCRIBE_PATH))
    # output_name = WAVE_OUTPUT_FILENAME + str(file_number) + FILE_EXTENSION
    output_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + FILE_EXTENSION
    wf = wave.open(output_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(AUDIO.get_sample_size(AUDIO_FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    try:
        shutil.move(BASE_PATH + output_name, TRANSCRIBE_PATH + output_name)
    except FileNotFoundError as fnf:
        print(fnf)


def record_audio(aud_conn, recording, frames):
    while True:
        if recording.is_set():
            data = aud_conn.recv(2048)
            frames.append(data)

def handle_client(cmd_conn, cmd_addr):
    try:
        frames = []
        recording = threading.Event()
        recording.clear()
        aud_conn, aud_addr = AUD_SERVERSOCKET.accept()
        aud_thread = threading.Thread(target=record_audio, args=(aud_conn, recording, frames))
        aud_thread.start()
        print(f"{aud_addr} Audio Socket Connected")
        while True:
            msg_len = cmd_conn.recv(HEADER).decode(DECODE_FORMAT)
            if msg_len:
                msg_len = int(msg_len)
                msg = cmd_conn.recv(msg_len).decode(DECODE_FORMAT)
                if msg == DISCONNECT_MSG:
                    print(f"{cmd_addr} Disconnected")
                    recording.clear()
                    frames.clear()
                elif msg == RECORD:
                    if recording.is_set():
                        print (f"{cmd_addr} {msg}")
                        continue
                    else:
                        print(f"{cmd_addr} Recording starting")
                        recording.set()
                elif msg == STOP:
                    if recording.is_set():
                        print(f"{cmd_addr} Recording stopped")
                        recording.clear()
                        create_wavfile(frames)
                        # print(transcribe.speech_to_text())
                        # print("Finished Transcribing")
                        frames.clear()
                    else:
                        print (f"{cmd_addr} {msg}")
                        continue
                else:
                    print (f"{cmd_addr} {msg}")
    except socket.error as msg:
        print(f"Socket Error: {msg}" )

def start():
    print("Server starting")
    CMD_SERVERSOCKET.listen()
    AUD_SERVERSOCKET.listen()
    print(f"Server ip {SERVER}")
    print(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    while True:
        cmd_conn, cmd_addr = CMD_SERVERSOCKET.accept()
        print(f"{cmd_addr} Command Socket Connected")
        cmd_thread = threading.Thread(target=handle_client, args=(cmd_conn, cmd_addr))
        cmd_thread.start()
    
if __name__ == "__main__":
    start()
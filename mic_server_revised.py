import pyaudio
import socket
import threading
import shutil
import wave

HEADER = 64
DECODE_FORMAT = "utf-8"
DISCONNECT_MSG = "quit"
RECORD = "record"
STOP = "stop"

AUDIO = pyaudio.PyAudio()
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

WAVE_OUTPUT_FILENAME = "output.wav"
BASE_PATH = "C:/Users/Devin/Videos/audiorecorder/"
TRANSCRIBE_PATH = "C:/Users/Devin/Videos/wav2/audio/"

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
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(AUDIO.get_sample_size(AUDIO_FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    shutil.move(BASE_PATH + WAVE_OUTPUT_FILENAME, TRANSCRIBE_PATH + WAVE_OUTPUT_FILENAME)

def record_audio(aud_conn, aud_addr, recording, frames):
    print(f"{aud_addr} Audio Socket Connected")
    while recording.is_set():
        data = aud_conn.recv(2048)
        frames.append(data)

def handle_client(cmd_conn, cmd_addr):
    print(f"{cmd_addr} Command Socket Connected")
    recording = threading.Event()
    recording.clear()
    frames = [] 
    aud_conn, aud_addr = AUD_SERVERSOCKET.accept()
    aud_thread = threading.Thread(target=record_audio, args=(aud_conn, aud_addr, recording, frames))
    aud_thread.start()
    while True:
        msg_len = cmd_conn.recv(HEADER).decode(DECODE_FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            msg = cmd_conn.recv(msg_len).decode(DECODE_FORMAT)
            if msg == DISCONNECT_MSG:
                print(f"{cmd_addr} Disconnected")
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
                    print(frames)
                    create_wavfile(frames)
                else:
                    print (f"{cmd_addr} {msg}")
                    continue
            else:
                print (f"{cmd_addr} {msg}")

def start():
    print("Server starting")
    CMD_SERVERSOCKET.listen()
    AUD_SERVERSOCKET.listen()
    print(f"Server ip {SERVER}")
    while True:
        cmd_conn, cmd_addr = CMD_SERVERSOCKET.accept()
        cmd_thread = threading.Thread(target=handle_client, args=(cmd_conn, cmd_addr))
        cmd_thread.start()
    
if __name__ == "__main__":
    start()
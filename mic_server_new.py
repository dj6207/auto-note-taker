import pyaudio
import socket
import wave
import threading

HEADER = 64
DECODE_FORMAT = 'utf-8'
DISCONNECT_MSG = "quit"
RECORD = "record"

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
WAVE_OUTPUT_FILENAME = "output.wav"

audio = pyaudio.PyAudio()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(ADDRESS)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        record_time = 0
        frames =[]
        msg_len = conn.recv(HEADER).decode(DECODE_FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(DECODE_FORMAT)
            if msg == DISCONNECT_MSG:
                print(f"[{addr}] disconnected")
                connected = False
            else:
                print (f"[{addr}] {msg}")
    conn.close()


# Handles new connections
def start():
    serversocket.listen()
    print(f"Server ip {SERVER}")
    while True:
        conn, addr = serversocket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


def main():
    print("Server starting")
    while True:
        start()

if __name__ == "__main__":
    main()
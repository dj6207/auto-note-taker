import pyaudio
import socket
import wave
import threading
import select



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

def record_audio(conn, time):
    frames = []
    print("Start Recording")
    while len(frames) <= time:
        print("recording")
        data = conn.recv(2000)
        frames.append(data)
        # print(f"server: {len(frames)}")
        # print(data)
    print("Finished recording")
    return frames



def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        msg_len = conn.recv(HEADER).decode(DECODE_FORMAT)
        # try:
        #     msg_len = conn.recv(HEADER).decode(DECODE_FORMAT)
        # except UnicodeDecodeError:
        #     msg_len = conn.recv(HEADER)
        #     print(f"message length stuff {msg_len}")
        #     msg_len = msg_len.decode(DECODE_FORMAT)
        # print(msg_len)  
        if msg_len:
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(DECODE_FORMAT)
            if msg == DISCONNECT_MSG:
                print(f"[{addr}] disconnected")
                connected = False
            elif msg.split(" ")[0] == RECORD:
                if (len(msg.split(" ")) == 2):
                    time = (int) (msg.split(" ")[1])
                    frames = record_audio(conn, time)
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
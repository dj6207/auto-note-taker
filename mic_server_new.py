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

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def record_audio(conn, time):
    frames = []
    print("Start Recording")
    while len(frames) <= time:
        printProgressBar(len(frames), time)
        data = conn.recv(2000)
        frames.append(data)
    print("Finished recording")
    return frames

def create_wavfile(frames):
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("Wav file generated")

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        msg_len = conn.recv(HEADER).decode(DECODE_FORMAT)
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
                    create_wavfile(frames)
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
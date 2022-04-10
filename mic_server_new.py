import pyaudio
import socket
import wave
import threading
import transcrib
import shutil

# Length of the message received
HEADER = 64
# Decoding format
DECODE_FORMAT = 'utf-8'
# Command that closes the connection with the client
DISCONNECT_MSG = "quit"
# Command that starts the audio recording
RECORD = "record"
# Bit Depth
FORMAT = pyaudio.paInt16
# Number of audio streams to use
CHANNELS = 1
# Number of samples of audio recorded every second (sample rate)
RATE = 44100
# Port number
PORT = 5050
# Server ip
SERVER = socket.gethostbyname(socket.gethostname())
# Server ip and Port
ADDRESS = (SERVER, PORT)
# Name of the output file
WAVE_OUTPUT_FILENAME = "output.wav"
# Instantiate PyAudio
audio = pyaudio.PyAudio()
# Path to where the audio file .wav file is made
BASE_PATH = "C:/Users/Devin/Videos/audiorecorder/"
# Path to where the audio file is moved to be formated, resampled, and transcribed
TRANSCRIBE_PATH = "C:/Users/Devin/Videos/wav2/audio/"
# Creates a server socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Binds the server socket to ADDRESS
serversocket.bind(ADDRESS)

def printProgressBar (iteration, total, prefix = 'Progress', suffix = 'Complete', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Prints the progress bar for the recording process
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
    if iteration == total: 
        print()

def record_audio(conn, time):
    """
    Function that recieves audio data from the client for a specific amount of time
    @params:
        conn    : The socket that allows for communication between server and client
        time    : Amount of time the server has to receive audio data
    @return:
        frames  : A list containing audio data
    """
    frames = []
    while len(frames) <= time:
        printProgressBar(len(frames), time)
        data = conn.recv(2000)
        frames.append(data)
    return frames

def create_wavfile(frames):
    """
    Creates a .wav file and moves the file in to the audio folder
    @params:
        frames  : A list containing audio data
    """
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    shutil.move(BASE_PATH + WAVE_OUTPUT_FILENAME, TRANSCRIBE_PATH + WAVE_OUTPUT_FILENAME)
    # print("Wav file generated")

def handle_client(conn, addr):
    """
    Handles the client conencted to the server
    Receives commands from the client
    Valid commands:
    - quit              : closes the client connection
    - record (seconds)  : starts receiving data from the client for a specified amoun of time
    @params:
        conn  : The socket that allows for communication between server and client
        addr  : Information about the conneciton (IP address, Port number)
    """
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
                    time = ((int) (msg.split(" ")[1])) * 45.3
                    frames = record_audio(conn, time)
                    create_wavfile(frames)
                    print(transcrib.speech_to_data())
            else:
                print (f"[{addr}] {msg}")
    conn.close()

def start():
    """
    Starts the mic_server
    Prints out the server ip and the numebr of active connections
    """
    print("Server starting")
    serversocket.listen()
    print(f"Server ip {SERVER}")
    while True:
        conn, addr = serversocket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

def main():
    start()

if __name__ == "__main__":
    main()
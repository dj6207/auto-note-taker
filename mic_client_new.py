import pyaudio
import socket

FORMAT = pyaudio.paInt16
CHANNELS = 1
# number of samples of audio recorded every second (sample rate)
RATE = 44100
# Number of frames in a buffer
CHUNK = 1000
# Port number
PORT = 5050
# Server ip
SERVER = socket.gethostbyname(socket.gethostname())
# Tuple of Server and Port
ADDR = (SERVER, PORT)

COMMANDS = ["- quit", "- record (seconds)"]

HEADER = 64
DECODE_FORMAT = 'utf-8'
DISCONNECT_MSG = "quit"
RECORD = "record"

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connects to the server
clientsocket.connect(ADDR)
audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

def printProgressBar (iteration, total, prefix = 'Progress', suffix = 'Complete', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
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

def send_audio(time):
    frames = []
    while True:
        data = stream.read(CHUNK)
        # print(f"data length {len(data)}")
        frames.append(data)
        # print(f"frames length: {len(frames)}")
        if len(frames) > time - 1:
            data = stream.read(CHUNK + 1)
            clientsocket.sendall(data)
            printProgressBar(len(frames), time)
            break
        else:
            clientsocket.send(data)
            printProgressBar(len(frames), time)

def send_msg(msg):
    message = msg.encode(DECODE_FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(DECODE_FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    clientsocket.send(send_len)
    clientsocket.send(message)

def main():
    while True:
        message = input("Input command: ")
        if message == DISCONNECT_MSG:
            send_msg(message)
            print("Client disconnect from server")
            break
        elif message.split(" ")[0] == RECORD:
            if (len(message.split(" ")) == 2):
                time = ((int) (message.split(" ")[1])) * 45.3
                send_msg(message)
                print("Recording")
                send_audio(time)
            else:
                print("record (seconds)")

        else:
            send_msg(message)
            print("Type a valid command")
            for item in COMMANDS:
                print(item)
    stream.close
    clientsocket.close
    audio.close

if __name__ == "__main__":
    main()
import pyaudio
import socket

# Bit Depth
FORMAT = pyaudio.paInt16
# Number of audio streams to use
CHANNELS = 1
# Number of samples of audio recorded every second (sample rate)
RATE = 44100
# Number of frames in a buffer
CHUNK = 1000
# Port number
PORT = 5050
# Server ip
SERVER = socket.gethostbyname(socket.gethostname())
# Server ip and Port
ADDR = (SERVER, PORT)
# Valid commands
COMMANDS = ["- quit", "- record (seconds)"]
# Length of the message received
HEADER = 64
# Encoding format
ENCODE_FORMAT = 'utf-8'
# Command that closes the connection with the client
DISCONNECT_MSG = "quit"
# Command that starts the audio recording
RECORD = "record"
# Creates a client socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connects to the server
clientsocket.connect(ADDR)
# Instantiate PyAudio
audio = pyaudio.PyAudio()
# Opens an audio stream
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

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

def send_audio(time):
    """
    Reads in data from the audio steam
    Sends audio data to the server for a certain amount of time
    @params:
        time  : Amount of time the client has to record and send audio data to the server
    """
    frames = []
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        if len(frames) > time - 1:
            data = stream.read(CHUNK + 1)
            clientsocket.send(data)
            printProgressBar(len(frames), time)
            break
        else:
            clientsocket.send(data)
            printProgressBar(len(frames), time)

def send_msg(msg):
    """
    Sends messages and commands to the server
    @params:
        msg  : message or commands that will be sent to the server
    """
    message = msg.encode(ENCODE_FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(ENCODE_FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    clientsocket.send(send_len)
    clientsocket.send(message)

def start():
    """
    Starts the client and promts user to input a command
    Valid commands:
    - quit              : closes the client connection
    - record (seconds)  : starts receiving data from the client for a specified amoun of time
    """
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
            print("Type a valid command:")
            for item in COMMANDS:
                print(item)
    stream.close
    clientsocket.close
    audio.close

def main():
    start()

if __name__ == "__main__":
    main()
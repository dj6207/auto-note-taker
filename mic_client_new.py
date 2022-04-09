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

HEADER = 64
DECODE_FORMAT = 'utf-8'
DISCONNECT_MSG = "quit"
RECORD = "record"

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connects to the server
clientsocket.connect(ADDR)
audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

def send_audio(time):
    frames = []
    while True:
        data = stream.read(CHUNK)
        print(f"data length {len(data)}")
        frames.append(data)
        print(f"client: {len(frames)}")
        if len(frames) > time - 1:
            data = stream.read(CHUNK + 1)
            clientsocket.sendall(data)
            break
        else:
            clientsocket.send(data)

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
            # send_msg(message)
            if (len(message.split(" ")) == 2):
                time = (int) (message.split(" ")[1])
                send_msg(message)
                print("Recording")
                send_audio(time)
                # while True:
                #     data = stream.read(CHUNK)
                #     frames.append(data)
                #     if len(frames) > time:
                #         break
                #     clientsocket.send(data)
            else:
                print("record (seconds)")

        else:
            send_msg(message)

if __name__ == "__main__":
    main()
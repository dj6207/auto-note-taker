import pyaudio
import socket
import threading


HEADER = 64
ENCODE_FORMAT = "utf-8"
DISCONNECT_MSG = "quit"
RECORD = "record"
STOP = "stop"

AUDIO = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16
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

def send_audio(aud_clientsocket, recording):
    aud_clientsocket.connect(AUD_ADDRESS)
    stream = AUDIO.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    while recording:
        data = stream.read(CHUNK)
        aud_clientsocket.send(data)
    # print("Send audio has stopped")
    # aud_clientsocket.close()

def send_msg(msg):
    message = msg.encode(ENCODE_FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(ENCODE_FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    CMD_CLIENTSOCKET.send(send_len)
    CMD_CLIENTSOCKET.send(message)

def server_comm(clientsocket):
    clientsocket.connect(CMD_ADDRESS)
    recording = False
    AUD_thread = threading.Thread(target=send_audio, args=(AUD_CLIENTSOCKET, recording))
    AUD_thread.start()
    while True:
        message = input("Input command: ")
        send_msg(message)
        if message == DISCONNECT_MSG:
            print("Disconnecting from server")
            break
        elif message == RECORD:
            print("Recording")
            recording = True
        elif message == STOP:
            print("Stop recording")
            recording = False
            AUD_thread.join()
            print("Thread Joined")
        else:
            print("Type a valid command:")
    clientsocket.close()

def start():
    CMD_thread = threading.Thread(target=server_comm, args=[CMD_CLIENTSOCKET])
    CMD_thread.start()

def main():
    start()

if __name__ == "__main__":
    main()
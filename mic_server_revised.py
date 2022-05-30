import pyaudio
import socket
import threading

HEADER = 64
DECODE_FORMAT = "utf-8"
DISCONNECT_MSG = "quit"
RECORD = "record"
STOP = "stop"

SERVER = socket.gethostbyname(socket.gethostname())
CMD_PORT = 5050
AUD_PORT = 5060
CMD_ADDRESS = (SERVER, CMD_PORT)
AUD_ADDRESS = (SERVER, AUD_PORT)
CMD_SERVERSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CMD_SERVERSOCKET.bind(CMD_ADDRESS)
AUD_SERVERSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
AUD_SERVERSOCKET.bind(AUD_ADDRESS)
 
def record_audio(aud_conn, aud_addr, recording):
    frames = []
    print(f"{aud_addr} recording")
    while recording:
        data = aud_conn.recv(2048)
        frames.append(data)
    # print("Record audio has stopped")

def handle_client(conn, addr):
    print(f"{addr} connected")
    connected = True
    recording = False
    aud_conn, aud_addr = AUD_SERVERSOCKET.accept()
    aud_thread = threading.Thread(target=record_audio, args=(aud_conn, aud_addr, recording))
    aud_thread.start()
    while connected:
        msg_len = conn.recv(HEADER).decode(DECODE_FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(DECODE_FORMAT)
            if msg == DISCONNECT_MSG:
                print(f"[{addr}] disconnected")
                connected = False
            elif msg == RECORD:
                recording = True
                print("Recording")
            elif msg == STOP:
                recording = False
                print("Recording stopped")
                aud_thread.join()
            else:
                print (f"[{addr}] {msg}")
    conn.close()


def start():
    print("Server starting")
    CMD_SERVERSOCKET.listen()
    AUD_SERVERSOCKET.listen()
    print(f"Server ip {SERVER}")
    while True:
        conn, addr = CMD_SERVERSOCKET.accept()
        cmd_thread = threading.Thread(target=handle_client, args=(conn, addr))
        cmd_thread.start()
    
def main():
    start()

if __name__ == "__main__":
    main()
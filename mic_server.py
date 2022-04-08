#!/usr/bin/env python

import pyaudio
import socket
import wave
import threading

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDRESS = (SERVER, PORT)
WAVE_OUTPUT_FILENAME = "output.wav"

audio = pyaudio.PyAudio()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(ADDRESS)
serversocket.listen(5)

try:
    while True:
        frames = []
        try:
            (clientsocket, ADDRESS) = serversocket.accept()
            print ("Connection from", ADDRESS)
            while True:
                data = clientsocket.recv(1024)
                frames.append(data)
        except serversocket.error:
            print ("finished recording")
except KeyboardInterrupt:
    pass


print ("Server Close")

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

serversocket.close()
# stop Recording
audio.terminate()

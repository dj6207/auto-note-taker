#!/usr/bin/env python

import pyaudio
import socket

FORMAT = pyaudio.paInt16
CHANNELS = 1
# number of samples of audio recorded every second (sample rate)
RATE = 44100
# Number of frames in a buffer
CHUNK = 4096
# Port number
PORT = 5050
# Server ip
SERVER = socket.gethostbyname(socket.gethostname())
# Tuple of Server and Port
ADDR = (SERVER, PORT)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connects to the server
serversocket.connect(ADDR)
audio = pyaudio.PyAudio()
# Starts audio stream
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
print ("recording...")
Total_chunk = 0

try:
    while True:
        line = input("quit")
        if line == "quit":
            serversocket.close
        data = stream.read(CHUNK)
        serversocket.send(data)
except serversocket.error:
    pass

print('Shutting down')
serversocket.close()
stream.close()
audio.terminate()

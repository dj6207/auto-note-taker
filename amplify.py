import pydub
from pydub.playback import play
import os

BASE_PATH = "C:/Users/frost/OneDrive/Documents/audiorecorder/Transcribe_Path/"
AMPLIFIED_PATH = "C:/Users/frost/OneDrive/Documents/audiorecorder/Amplified/"
FILE_FROMAT = "wav"


def play_audio(file): 
    audio = pydub.AudioSegment.from_file(file= BASE_PATH + file, format=FILE_FROMAT)
    print("Playing audio")
    play(audio)


def amplify(file):
    file_name, file_extension = os.path.splitext(file)
    audio = pydub.AudioSegment.from_file(file= BASE_PATH + file, format=FILE_FROMAT)
    amplified = audio + 15
    amplified.export(AMPLIFIED_PATH + file_name + "_Amplified" + file_extension, format= FILE_FROMAT)    
    return amplified

if __name__ == "__main__":
    try:
        file = input("File Name: ") 
        # play_audio(file)
        amp_file = amplify(file)
        print("Play amplified audio")
        play(amp_file)
    except FileNotFoundError as fnf:
        print(fnf)
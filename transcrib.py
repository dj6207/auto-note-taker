import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import librosa
import os
import soundfile as sf
import datetime
from datetime import date
import shutil
import subprocess

# Sample rate of the audio that will be transcribed
# Uses 16000 hz unstead of the normal 44100 hz or 48000 hz because wav2vec is trained on 16000 hz data
sr = 16000

# Chunk size for each chunk of audio
# block_length is set to 30 to break the audio in to 30 second chunks
block_length = 30

# Path to the audio location
path_base = "C:/Users/Devin/Videos/wav2/audio/"

# Path to the converted audio location
path_converted_audio = "C:/Users/Devin/Videos/wav2/pathconverted/"

# Path to the resampled audio location
resampled_folder = "C:/Users/Devin/Videos/wav2/resampled/"

# Path to the audio report
audio_report = "C:/Users/Devin/Videos/wav2/audioreport/"

# File types that will be converted to wav
extension_to_convert = ['.mp3','.mp4']

# Speech to text processor and model
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")

def printProgressBar (iteration, total, prefix = 'Progress', suffix = 'Complete', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Prints the progress bar for transcription process
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

def preprocessing(path_base, path_converted_audio):
    """
    Wav2Vec only support wav file so non .wav files need to be converted. Checks time files in the path_base folder. 
    If file is right format the file will be moved to the converted folder.
    If file is not the right format the will be converted to .wav file using ffmpeg and moved to the converted folder.
    If the file type is not in the supported file type list, prints out an error
    @params:
        path_base             : path to the folder with the audio files
        path_converted_audio  : path to the folder with the audio files with the right file type
    """
    for file in os.listdir(path_base):
        filename, file_extension = os.path.splitext(file)
        print("\nFile name: " + file)
        if file_extension == ".wav":
            shutil.copy(path_base + file, path_converted_audio + file)
        elif file_extension in extension_to_convert:
            subprocess.call(['ffmpeg', '-i', path_base + file,
            path_base + filename + ".wav"])
            shutil.move(path_base + filename + ".wav", path_converted_audio + filename + ".wav")
            print(file + " is converted into " + filename +".wav")
        else:
            print("ERROR: Unsupported file type")

def resample(file, sr): 
    """
    Wav2Vec is trained using data that is 16000 hz so the .wav file needs to be converted to 16000 hz.
    Gets the file from the converted folder and resamples them to 16000 hz
    Makes the resampled audio file in the resampled foler
    @params:
        file            : file that will be resampled
        sr              : the final sample rate of the audio file which is 16000 hz
    @return:
        resampled_path  : path to the individual resampled file
        length          : length of the audio file
    """
    path = path_converted_audio + file
    audio, sr = librosa.load(path, sr=sr) 
    length = librosa.get_duration(audio, sr)
    sf.write(os.path.join(resampled_folder,file), audio, sr) 
    resampled_path = os.path.join(resampled_folder,file) 
    return resampled_path, length

def asr_transcript(processor, model, resampled_path, length, block_length):
    """
    Breaks down the audio file into 30 second chunks instead of loading the full audio file
    Passes the 30 second chunk to the generate transciption generator 
    Contatenates the output from trascription generator
    @params:
        processor       : Wav2vec processor
        model           : Wav2vec model
        resampled_path  : audio file path in the resampled folder
        length          : length of the audio file
        block_length    : length of each chunk in seconds
    @return:
        transcript      : generated transcription as a string
    """
    chunks = length//block_length
    if length % block_length != 0:
        chunks += 1
    transcript = ""   
    stream = librosa.stream(resampled_path, block_length=block_length, frame_length=16000, hop_length=16000)
    for n, speech in enumerate(stream):
        separator = ' '
        if n % 2 == 0:
            separator = '\n'
        transcript += generate_transcription(speech, processor, model) + separator
        printProgressBar(n+1, chunks)
    return transcript

def generate_transcription(speech, processor, model):
    """
    Generates the transcription using Wav2vec processor and model
    @params:
        speech         : audio chunk that is going to be transcirbed
        processor      : Wav2vec processor
        model          : Wav2vec model
    @return:
        transcription  : generated transcription of the chunk as a string
    """
    if len(speech.shape) > 1:
        speech = speech[:, 0] + speech[:, 1]   
    input_values = processor(speech, sampling_rate = sr, return_tensors="pt").input_values
    logits = model(input_values).logits             
    predicted_ids = torch.argmax(logits, dim=-1)       
    transcription = processor.decode(predicted_ids[0])
    return transcription.lower()

def generate_textfile(transcript, audio_report, file, length):
    """
    Generates a text file of the transcription
    Contains file name, date, length of the audio, path to the audio file
    Saves the text file transcript in the audio report audio report folder
    @params:
        transcript    : transcription
        audio_report  : path to the audio report folder
        file          : audio file
        length        : length of the audio file
    """
    today = date.today()
    report = f"REPORT\nFile name: {file}\nDate: {today}" \
         f"\nLength: {datetime.timedelta(seconds=round(length,0))}" \
         f"\nFile stored at: {os.path.join(audio_report, file)}.txt\n"
    report += transcript   
    filepath = os.path.join(audio_report,file)
    text = open(filepath + ".txt","w")
    text.write(report)
    text.close()
    print("\nReport stored at " + filepath + ".txt")

def speech_to_data():
    """
    Main function that runs all the processes
    @return:
        transcript  : transcription
    """
    preprocessing(path_base, path_converted_audio)
    for file in os.listdir(path_converted_audio):
        resampled_path, length = resample(file, sr)
        transcript = asr_transcript(processor, model, resampled_path, length, block_length)
        generate_textfile(transcript, audio_report, file, length)
    return transcript
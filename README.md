# Auto-Note-Taker
Auto Note Taker uses the Wav2vec's automatic speech recognition model to transcribe audio to readable text. This project uses pyaudio and sockets to record and stream audio to a server to transcribe in to text. This repository conatins code for the mic_server, the mic_client, and the transcription. 

# Required libraries
- pyaudio
- socket
- wave
- threading
- shutil
- torch
- librosa
- os
- soundfile
- datetime
- subprocess
- transformers

Link to download pyaudio: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

Link to download pytorch: https://pytorch.org/

Link to Wav2vec models: https://huggingface.co/models?filter=wav2vec2

# How to use
Change the folder paths in both mic_client_new.py and mic_server_new.py

Run mic_server_new.py

Change the Server ip to the ip of your server in mic_client_new.py

Run mic_client_new.py

Start recording audio

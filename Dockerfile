FROM python:3.7.9

WORKDIR /usr/scr/app

COPY server.py .

RUN apt-get update
RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y
RUN pip install pyaudio

CMD ["python", "./server.py"]

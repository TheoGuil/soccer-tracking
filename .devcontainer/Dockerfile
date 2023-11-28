FROM python:3.10

COPY requirements.txt dependencies/requirements.txt

RUN pip install -r dependencies/requirements.txt

RUN apt update -y && apt upgrade -y

RUN apt install -y ffmpeg
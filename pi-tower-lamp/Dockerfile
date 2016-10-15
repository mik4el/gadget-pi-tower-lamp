FROM resin/raspberrypi-python:3.5-slim
COPY requirements.txt /
Run apt-get update
RUN apt-get install -y libjpeg8-dev zlib1g-dev
RUN pip install -r requirements.txt

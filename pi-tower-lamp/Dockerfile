FROM resin/raspberrypi-python:3.5-slim
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
COPY requirements.txt /usr/src/app/
Run apt-get update
RUN apt-get install -y libjpeg8-dev zlib1g-dev
RUN pip install -r requirements.txt

FROM python:3.5-onbuild
COPY . /
RUN apt-get --yes --force-yes install libjpeg-dev zlib1g-dev
RUN pip install -r requirements.txt

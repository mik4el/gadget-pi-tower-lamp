# README for PI Tower Lamp
Controlling a circuit of rgb leds in a lamp to show average color of the windows in the Telefonplan Tower from a webcam image using a RaspberryPI and Python. When a significant change of the average color happens the lamp animates to the new color. Also runs a simulation of lamp color, input colors and enhanced webcam image for testing purposes.

## Dependencies
Python 3.5, pillow, pi-blaster, requests, Docker, docker-compose

## Tests
Run tests with this command:

```
cd pi-tower-lamp
python -m unittest tests
```

## Running it
The program can be run in visual mode for developing and debugging and in rgbled mode to control rgb leds.

### First time on pi
1. Install pi-blaster (https://github.com/sarfata/pi-blaster or my fork that works with gpio pins 2,3 and 4 from https://github.com/mik4el/pi-blaster).
1. `docker-compose up -d`

### For developing:
```
cd pi-tower-lamp
python main.py --mode visual
```

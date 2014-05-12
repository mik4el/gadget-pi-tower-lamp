# README for PI Tower Lamp
Controlling a circuit of rgb leds in a lamp to show average color of in windows of the Telefonplan Tower from a webcam image using a RaspberryPI and Python. Also runs a simulation of lamp color, input colors and enhanced webcam image for testing purposes.
When a significant change of the average color happens the lamp animates to the new color.

### Tests
Run tests with this command:
python -m unittest tests

### Running it
The program can be run in visual mode for developing and debugging and in rgbled mode to control rgb leds.

####On pi in ~/pi_tower_lamp:
./../env/bin/python main.py --mode rgbled > log.txt

####For developing:
python main.py --mode visual

### Dependencies
Python 2.7, pillow, fabric, fabtools, git-archive-all, rpi.gpio, git, pi-blaster, requests, supervisor

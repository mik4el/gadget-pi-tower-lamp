# README for PI Tower Lamp
Controlling a circuit of rgb leds to match colors in windows of the Telefonplan Tower from a webcam image using a RaspberryPI and Python. Also runs a simulated light led in commandline for testing purpose.
When a color changes in the Tower the lamp goes through the ten new colors in sequence and ends with average color.

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
Python 2.7, pillow, fabric, fabtools, git-archive-all, rpi.gpio, git, pi-blaster, requests

### Todo
1. Write test suite to lock down behaviour for release
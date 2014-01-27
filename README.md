# README for PI Tower Lamp
Controlling a circuit of rgb leds to match colors in windows of the Telefonplan Tower from a webcam image using a RaspberryPI and Python. Also runs a simulated light led in commandline for testing purpose.
When a color changes in the Tower the lamp goes through the ten new colors in sequence and ends with average color.

### Tests
Run tests with this command:
python -m unittest tests

### Dependencies
Python 2.7, PIL, curl

### Todo
1. Make filter to detect a significant enough change in tower average color
1. Install raspi
1. Setup deployment to raspi with fabfile
1. Build and control circuit to control one light on/off
1. Build and control circuit to control one rgb light without PWM
1. Build and control circuit to control one rgb light with PWM
1. Make animation for ten window colors before animating to average color
1. Build circuit to control lights with external power
1. Finalize product and hook up in window
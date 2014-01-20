# README for PI Tower Lamp
Controlling a circuit of rgb leds to match colors in windows of the Telefonplan Tower from a webcam image using a RaspberryPI and Python. Also runs a simulated light led in commandline for testing purpose.
When a color changes in the Tower the lamp goes through the ten new colors in sequence and ends with average color.

### Tests
TestRGBForPixel tests that function RGBForPixel works.

Run tests with this command:
python -m unittest tests

### Todo
1. Find pixel position of window's center in webcam image for all ten windows
1. Read test image and print colors per window for all ten windows in image
1. Visualize the ten colors in commandline
1. Get average color from ten colors and visualize
1. Simulate in commandline behaviour of led
1. Download image from online
1. Simulate how the light looks realtime
1. Build circuit to control one light
1. Control real light
1. Build circuit to control lights with external power
1. Finalize product and hook up in window
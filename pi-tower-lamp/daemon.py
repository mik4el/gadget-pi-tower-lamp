import time
import RPi.GPIO as GPIO
import signal
import sys


class PITowerLampRGBLED:
    def __init__(self, towerControllerQueue, lampControllerQueue):
        self.towerControllerQueue = towerControllerQueue
        self.lampControllerQueue = lampControllerQueue
        self.lampModel = None
        # Setup GPIOs
        GPIO.setmode(GPIO.BOARD)
        pin_red = 3
        pin_green = 5
        pin_blue = 7
        GPIO.setup(pin_red, GPIO.OUT)
        GPIO.setup(pin_green, GPIO.OUT)
        GPIO.setup(pin_blue, GPIO.OUT)
        freq = 100  # Hz
        self.red = GPIO.PWM(pin_red, freq)
        self.red.start(0)  # Initial duty cycle of 0, so off
        self.green = GPIO.PWM(pin_green, freq)
        self.green.start(0)
        self.blue = GPIO.PWM(pin_blue, freq)
        self.blue.start(0)
        self.redScaling = 1.0
        self.greenScaling = 0.2
        self.blueScaling = 0.1

        if sys.argv[1] == "handle_signal":
            signal.signal(signal.SIGTERM, self.sigterm_handler)

    def sigterm_handler(self, _signo, _stack_frame):
        # Raises SystemExit(0):
        sys.exit(0)

    def cleanup(self):
        print("Exiting PITowerLampRGBLED")
        self.red.stop()
        self.green.stop()
        self.blue.stop()
        GPIO.cleanup()
        exit()

    def start(self):
        try:
            while True:
                # Only redraw if new item in controllerQueue
                if not self.lampControllerQueue.empty():
                    self.lampModel = self.lampControllerQueue.get()
                    self.redraw()
                    if not self.towerControllerQueue.empty():
                        # avoid memory leak
                        tower_model = self.towerControllerQueue.get()
                        del tower_model
                time.sleep(0.01)
        finally:
            self.cleanup(self)

    def redraw(self):
        # Draw lampModel
        if self.lampModel:
            if self.lampModel.isOn:
                self.set_light(self.lampModel.getRGB())
            else:
                self.set_light((0, 0, 0))
        print("Canvas redrawn!")

    def set_light(self, rgb):
        print("setting", rgb)
        self.red.ChangeDutyCycle((float(rgb[0]) / 255.0)*self.redScaling*100.0)
        self.green.ChangeDutyCycle((float(rgb[1]) / 255.0)*self.greenScaling*100.0)
        self.blue.ChangeDutyCycle((float(rgb[2]) / 255.0)*self.blueScaling*100.0)

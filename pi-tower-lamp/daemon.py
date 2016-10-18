import time
import RPi.GPIO as GPIO


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
        freq = 1000  # Hz
        self.red = GPIO.PWM(pin_red, freq)
        self.red.start(0)  # Initial duty cycle of 0, so off
        self.green = GPIO.PWM(pin_green, freq)
        self.green.start(0)
        self.blue = GPIO.PWM(pin_blue, freq)
        self.blue.start(0)
        self.redScaling = 1.0
        self.greenScaling = 0.4
        self.blueScaling = 0.1

    def start(self):
        while True:
            try:
                # Only redraw if new item in controllerQueue
                if not self.lampControllerQueue.empty():
                    self.lampModel = self.lampControllerQueue.get()
                    self.redraw()
                    if not self.towerControllerQueue.empty():
                        # avoid memory leak
                        tower_model = self.towerControllerQueue.get()
                        del tower_model
            except KeyboardInterrupt:
                print("Exiting!")
                self.red.stop()
                self.green.stop()
                self.blue.stop()
                GPIO.cleanup()
                exit()

    def redraw(self):
        # Draw lampModel
        if self.lampModel:
            if self.lampModel.isOn:
                self.set_light(self.lampModel.getRGB())
            else:
                self.set_light((0, 0, 0))

    def set_light(self, rgb):
        print("Setting", rgb)
        self.red.ChangeDutyCycle((float(rgb[0]) / 255.0) * self.redScaling * 100.0)
        self.green.ChangeDutyCycle((float(rgb[1]) / 255.0) * self.greenScaling * 100.0)
        self.blue.ChangeDutyCycle((float(rgb[2]) / 255.0) * self.blueScaling * 100.0)

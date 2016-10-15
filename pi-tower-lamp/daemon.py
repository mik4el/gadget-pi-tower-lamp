import os
import time


class PITowerLampRGBLED:
    def __init__(self, towerControllerQueue, lampControllerQueue):
        self.towerControllerQueue = towerControllerQueue
        self.lampControllerQueue = lampControllerQueue
        self.lampModel = None
        self.pins = [4, 17, 18]
        self.redScaling = 1.0
        self.greenScaling = 0.2
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
                        towerModel = self.towerControllerQueue.get()
                        del towerModel
                time.sleep(0.01)
            except KeyboardInterrupt:
                print("Exiting!")
                for p in self.pins:
                    os.system('echo "%d=0" > /dev/pi-blaster' % p)
                    os.system('echo "release %d" > /dev/pi-blaster' % p)
                exit()

    def redraw(self):
        # Draw lampModel
        if self.lampModel:
            if self.lampModel.isOn:
                self.setLight(self.lampModel.getRGB())
            else:
                self.setLight((0, 0, 0))
        print("Canvas redrawn!")

    def setLight(self, rgb):
        print("setting", rgb)
        os.system(self.pi_blasterCommandForInput(self.pins[0], ((float(rgb[0]) / 255.0)*self.redScaling)))
        os.system(self.pi_blasterCommandForInput(self.pins[1], ((float(rgb[1]) / 255.0)*self.greenScaling)))
        os.system(self.pi_blasterCommandForInput(self.pins[2], ((float(rgb[2]) / 255.0)*self.blueScaling)))

    def pi_blasterCommandForInput(self, pin, value):
        return 'echo "%d=%.2f" > /dev/pi-blaster' % (pin, value)

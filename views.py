from helpers import hexFromRGB
from Tkinter import *
from PIL import ImageTk
import time
import os


class PITowerLampVisualization:
    def __init__(self, towerControllerQueue, lampControllerQueue):
        self.towerControllerQueue = towerControllerQueue
        self.lampControllerQueue = lampControllerQueue
        self.towerModel = None
        self.lampModel = None
        self.root = None
        self.canvas = None

    def start(self):
        # Start Tkinter
        self.root = Tk()
        self.root.title("PI Tower Lamp Visualization")

        # Draw GUI
        self.canvas = Canvas(self.root, width=1250, height=1000)
        self.canvas.pack()
        self.root.after(0, self.updateLoop())
        self.root.mainloop()

    def updateLoop(self):
        while True:
            # Only redraw if new item in controllerQueue
            if not self.towerControllerQueue.empty():
                self.towerModel = self.towerControllerQueue.get()
            if not self.lampControllerQueue.empty():
                self.lampModel = self.lampControllerQueue.get()
            self.redraw()
            time.sleep(0.01)

    def redraw(self):
        # Draw lampModel
        if self.lampModel:
            if self.lampModel.isOn:
                self.canvas.create_rectangle(250, 550, 450, 650, fill=hexFromRGB(self.lampModel.getRGB()))
            else:
                self.canvas.create_rectangle(250, 550, 450, 650, fill="#000000")

        # Draw towerModel
        if self.towerModel:
            # Draw windows
            for i in range(10):
                self.canvas.create_rectangle(0, 100*i, 200, 100*(1+i), fill=str(hexFromRGB(self.towerModel.allWindowsRGB[9-i])))

            # Draw average RGB block
            self.canvas.create_rectangle(250, 350, 450, 450, fill=hexFromRGB(self.towerModel.averageWindowRGB))

            # Draw tower visualization
            tkImage = ImageTk.PhotoImage(self.towerModel.image)
            self.canvas.create_image(900, 500, image=tkImage)

            self.canvas.update()
        print "Canvas redrawn!"


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
                print "Exiting!"
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
        print "Canvas redrawn!"

    def setLight(self, rgb):
        print "setting",  rgb
        os.system(self.pi_blasterCommandForInput(self.pins[0], ((float(rgb[0]) / 255.0)*self.redScaling)))
        os.system(self.pi_blasterCommandForInput(self.pins[1], ((float(rgb[1]) / 255.0)*self.greenScaling)))
        os.system(self.pi_blasterCommandForInput(self.pins[2], ((float(rgb[2]) / 255.0)*self.blueScaling)))

    def pi_blasterCommandForInput(self, pin, value):
        return 'echo "%d=%.2f" > /dev/pi-blaster' % (pin, value)
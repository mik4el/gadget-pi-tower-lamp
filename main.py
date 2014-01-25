from Tkinter import *
from PIL import Image, ImageTk
import os
import time
import threading
import Queue


def RGBForPixel(x, y, pixelsInImage):
    return pixelsInImage[x, y]


def RGBForWindow(windowNumber, pixelsInImage):
    POSITION_FOR_WINDOW_NUMBER = {
        0: [440, 299],
        1: [440, 277],
        2: [440, 255],
        3: [440, 234],
        4: [440, 212],
        5: [441, 189],
        6: [441, 169],
        7: [441, 148],
        8: [441, 126],
        9: [440, 105],
    }
    x = POSITION_FOR_WINDOW_NUMBER[windowNumber][0]
    y = POSITION_FOR_WINDOW_NUMBER[windowNumber][1]
    return RGBForPixel(x, y, pixelsInImage)


def RGBForAllWindows(pixelsInImage):
    allRGB = []
    for i in range(10):
        allRGB.append(RGBForWindow(i, pixelsInImage))
    return allRGB


def averageRGB(arrayOfRGB):
    R = 0
    G = 0
    B = 0
    for i in range(len(arrayOfRGB)):
        R += arrayOfRGB[i][0]
        G += arrayOfRGB[i][1]
        B += arrayOfRGB[i][2]
    R /= len(arrayOfRGB)
    G /= len(arrayOfRGB)
    B /= len(arrayOfRGB)
    return R, G, B


def hexFromRGB(RGB):
    return '#%02x%02x%02x' % RGB


class PILampModel:
    def __init__(self, rgb, isOn):
        self.rgb = rgb
        self.isOn = isOn
        print "Lamp model created!"


class PITowerModel:
    def __init__(self, allWindowsRGB, averageWindowRGB, image):
        self.allWindowsRGB = allWindowsRGB
        self.averageWindowRGB = averageWindowRGB
        self.image = image
        print "Tower model created!"


class PITowerController(threading.Thread):
    def __init__(self, imageName, towerControllerQueue, lampControllerQueue):
        threading.Thread.__init__(self)
        self.imageName = imageName
        self.image = None
        self.towerControllerQueue = towerControllerQueue
        self.lampControllerQueue = lampControllerQueue
        self.currentTowerModel = None
        self.currentLampModel = None
        self.ticks = 0
        self.tickTowerUpdate = 0
        self.tickLampUpdate = 0

    def downloadTowerImage(self):
        #os.system("curl -o tower_temp.jpg http://89.253.86.245//axis-cgi/jpg/image.cgi?resolution=800x450")
        self.simulateDownloadTowerImage()
        print "downloaded"

    def simulateDownloadTowerImage(self):
        if self.imageName == "tower_test_01.jpg":
            self.imageName = "tower_test_02.jpg"
        else:
            self.imageName = "tower_test_01.jpg"

    def updateTower(self):
        # Download new image
        self.downloadTowerImage()

        # Load image and get data
        self.image = Image.open(self.imageName)
        pixelsInImage = self.image.load()
        allWindowsColor = RGBForAllWindows(pixelsInImage)
        averageColor = averageRGB(allWindowsColor)

        # Create PITowerModel and put in towerControllerQueue
        towerModel = PITowerModel(allWindowsColor, averageColor, self.image)
        self.towerControllerQueue.put(towerModel)
        self.currentTowerModel = towerModel

    def updateLamp(self):
        # Create PILampModel and put in lampControllerQueue
        if self.ticks % 3 == 0:
            lampModel = PILampModel(self.currentTowerModel.averageWindowRGB, False)
            self.lampControllerQueue.put(lampModel)
            self.currentLampModel = lampModel
        else:
            lampModel = PILampModel(self.currentTowerModel.averageWindowRGB, True)
            self.lampControllerQueue.put(lampModel)
            self.currentLampModel = lampModel

    def tick(self):
        if self.ticks == self.tickTowerUpdate + 100 or self.ticks == 0:
            self.tickTowerUpdate = self.ticks
            self.updateTower()
        if self.ticks == self.tickLampUpdate + 10 or self.ticks == 0:
            self.tickLampUpdate = self.ticks
            self.updateLamp()
        self.ticks += 1
        time.sleep(0.1)
        print self.ticks

    def run(self):
        while True:
            self.tick()


class PITowerLampVisualization:
    def __init__(self, towerControllerQueue, lampControllerQueue):
        self.towerControllerQueue = towerControllerQueue
        self.lampControllerQueue = lampControllerQueue
        self.towerModel = None
        self.lampModel = None

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
                self.canvas.create_rectangle(250, 550, 450, 650, fill=hexFromRGB(self.lampModel.rgb))
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

# Create controller queue for communication between controller and view
towerControllerQueue = Queue.Queue()
lampControllerQueue = Queue.Queue()

# Create and start controller
controllerThread = PITowerController("tower_temp.jpg", towerControllerQueue, lampControllerQueue)
controllerThread.daemon = True
controllerThread.start()

# Create and start visualization view
visualization = PITowerLampVisualization(towerControllerQueue, lampControllerQueue)
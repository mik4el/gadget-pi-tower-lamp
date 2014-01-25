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

    def downloadTowerImage(self):
        os.system("curl -o tower_temp.jpg http://89.253.86.245//axis-cgi/jpg/image.cgi?resolution=800x450")

    def run(self):
        count = 0

        while True:
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

            # Create PILampModel and put in lampControllerQueue
            lampModel = PILampModel(averageColor, True)
            self.lampControllerQueue.put(lampModel)

            time.sleep(1)


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
            time.sleep(1/100)

    def redraw(self):
        # Draw lampModel
        if self.lampModel:
            if self.lampModel.isOn:
                self.canvas.create_rectangle(250, 650, 450, 750, fill=hexFromRGB(self.lampModel.rgb))
            else:
                self.canvas.create_rectangle(250, 650, 450, 750, fill="#000000")

        # Draw towerModel
        if self.towerModel:
            # Draw windows
            for i in range(10):
                self.canvas.create_rectangle(0, 100*i, 200, 100*(1+i), fill=str(hexFromRGB(self.towerModel.allWindowsRGB[9-i])))

            # Draw average RGB block
            self.canvas.create_rectangle(250, 450, 450, 550, fill=hexFromRGB(self.towerModel.averageWindowRGB))

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
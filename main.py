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


class PITowerModel:
    def __init__(self, allWindowsRGB, averageWindowRGB, image):
        self.allWindowsRGB = allWindowsRGB
        self.averageWindowRGB = averageWindowRGB
        self.image = image
        print "Tower model created!"


class PITowerController(threading.Thread):
    def __init__(self, imageName, controllerQueue):
        threading.Thread.__init__(self)
        self.imageName = imageName
        self.image = None
        self.controllerQueue = controllerQueue

    def downloadTowerImage(self):
        os.system("curl -o tower_temp.jpg http://89.253.86.245//axis-cgi/jpg/image.cgi?resolution=800x450")

    def run(self):
        while True:
            #Download new image
            self.downloadTowerImage()

            #Load image and get data
            self.image = Image.open(self.imageName)
            pixelsInImage = self.image.load()
            allWindowsRGB = RGBForAllWindows(pixelsInImage)

            #Create TowerModel and put in controllerQueue
            towerModel = PITowerModel(allWindowsRGB, averageRGB(allWindowsRGB), self.image)
            self.controllerQueue.put(towerModel)
            print "New tower model in queue!"
            time.sleep(5)


class PITowerLampVisualization:
    def __init__(self, controllerQueue):
        self.controllerQueue = controllerQueue

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
            if not controllerQueue.empty():
                self.towerModel = self.controllerQueue.get()
                self.redraw()
            time.sleep(1/100)

    def redraw(self):
        # Return if no towerModel
        if not self.towerModel:
            return

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

#Create controller queue for communication between controller and view
controllerQueue = Queue.Queue()

controllerThread = PITowerController("tower_temp.jpg", controllerQueue)
controllerThread.daemon = True
controllerThread.start()

visualization = PITowerLampVisualization(controllerQueue)
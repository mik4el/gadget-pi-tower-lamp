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
    def __init__(self, r, g, b, isOn):
        self.r = r
        self.g = g
        self.b = b
        self.isOn = isOn
        print "Lamp model created!"

    def getRGB(self):
        return self.r, self.g, self.b


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
        self.oldTowerModel = None
        self.currentLampModel = PILampModel(255, 255, 255, True)
        self.ticks = 0
        self.tickTowerUpdate = 0
        self.tickLampUpdate = 0
        self.updateHZ = 0.1
        self.deltaR = 0.0
        self.deltaG = 0.0
        self.deltaB = 0.0
        self.lampIsAnimating = False

    def startLampAnimation(self):
        print "Start lamp animation"
        startRGB = self.currentLampModel.getRGB()
        endRGB = self.currentTowerModel.averageWindowRGB
        steps = 1/self.updateHZ

        #Calculate deltas for RGB channels
        self.deltaR = float((endRGB[0]-startRGB[0]))/float(steps)
        self.deltaG = float((endRGB[1]-startRGB[1]))/float(steps)
        self.deltaB = float((endRGB[2]-startRGB[2]))/float(steps)

        #Start animation
        self.lampIsAnimating = True

    def checkLampAnimationReady(self):
        readyRGB = self.currentTowerModel.averageWindowRGB

        #Check if self.currentLampModel matches with readyRGB, set deltas to zero if match
        diffR = readyRGB[0] - self.currentLampModel.r
        if diffR >= 1 or diffR >= 1:
            self.deltaR = 0.0
            self.currentLampModel.r = readyRGB[0]
        diffG = readyRGB[1] - self.currentLampModel.g
        if diffG >= 1 or diffG >= 1:
            self.deltaG = 0.0
            self.currentLampModel.g = readyRGB[1]
        diffB = readyRGB[2] - self.currentLampModel.b
        if diffB >= 1 or diffB >= 1:
            self.deltaB = 0.0
            self.currentLampModel.b = readyRGB[2]

        #If all deltas == 0.0 then animation is over
        if self.deltaR == 0.0 and self.deltaG == 0.0 and self.deltaB == 0.0:
            self.lampIsAnimating = False

    def updateLamp(self):
        if self.lampIsAnimating:
            # Add deltas to lamp
            self.currentLampModel.r += self.deltaR
            self.currentLampModel.g += self.deltaG
            self.currentLampModel.b += self.deltaB

            # Check if ready
            self.checkLampAnimationReady()

            # Add new lamp to controller queue
            self.lampControllerQueue.put(self.currentLampModel)

    def towerModelChanged(self, newTowerModel):
        self.oldTowerModel = self.currentTowerModel
        self.currentTowerModel = newTowerModel
        self.towerControllerQueue.put(self.currentTowerModel)
        self.startLampAnimation()

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

        # Create PITowerModel and mark as changed
        towerModel = PITowerModel(allWindowsColor, averageColor, self.image)

        # Check if PITowerModel changed
        if self.currentTowerModel:
            if towerModel.averageWindowRGB != self.currentTowerModel.averageWindowRGB:
                self.towerModelChanged(towerModel)
        else:
            self.currentTowerModel = towerModel
            self.towerModelChanged(towerModel)

    def tick(self):
        if self.ticks == self.tickTowerUpdate + 5/self.updateHZ or self.ticks == 0:
            self.tickTowerUpdate = self.ticks
            self.updateTower()
        self.updateLamp()  # lamp should update as often as possible
        self.ticks += 1
        time.sleep(self.updateHZ)
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

# Create controller queue for communication between controller and view
towerControllerQueue = Queue.Queue()
lampControllerQueue = Queue.Queue()

# Create and start controller
controllerThread = PITowerController("tower_temp.jpg", towerControllerQueue, lampControllerQueue)
controllerThread.daemon = True
controllerThread.start()

# Create and start visualization view
visualization = PITowerLampVisualization(towerControllerQueue, lampControllerQueue)
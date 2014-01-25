import os
import threading
import time
from PIL import Image
from models import PILampModel, PITowerModel


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

        # Create PITowerModel and mark as changed
        towerModel = PITowerModel(self.image)

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
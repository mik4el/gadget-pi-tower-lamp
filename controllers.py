import os
import threading
import time
from PIL import Image, ImageFilter
from models import PILampModel, PITowerModel


class PITowerController(threading.Thread):

    def __init__(self, imageName, towerControllerQueue, lampControllerQueue):
        threading.Thread.__init__(self)
        self.imageName = imageName
        self.isSimulating = False
        if self.imageName != "tower_temp.jpg":
            self.isSimulating = True
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
        self.animationDeltaR = 0.0
        self.animationDeltaG = 0.0
        self.animationDeltaB = 0.0
        self.lampIsAnimating = False
        self.animationSteps = 0
        self.animationStartRGB = None
        self.animationEndRGB = None
        self.towerChangedTreshold = 0.10

    def startLampAnimation(self):
        # Setup input variables
        self.animationStartRGB = self.currentLampModel.getRGB()
        self.animationEndRGB = self.currentTowerModel.averageWindowRGB
        self.animationSteps = 1/self.updateHZ

        # Calculate deltas for RGB channels
        self.animationDeltaR = float((self.animationEndRGB[0]-self.animationStartRGB[0]))/float(self.animationSteps)
        self.animationDeltaG = float((self.animationEndRGB[1]-self.animationStartRGB[1]))/float(self.animationSteps)
        self.animationDeltaB = float((self.animationEndRGB[2]-self.animationStartRGB[2]))/float(self.animationSteps)

        # Start animation
        self.lampIsAnimating = True

    def checkLampAnimationReady(self):
        readyRGB = self.currentTowerModel.averageWindowRGB

        #Check if self.currentLampModel matches with readyRGB, set deltas to zero if match
        diffR = readyRGB[0] - self.currentLampModel.r
        if abs(diffR) <= 1:
            self.animationDeltaR = 0.0
            self.currentLampModel.r = readyRGB[0]
        diffG = readyRGB[1] - self.currentLampModel.g
        if abs(diffG) <= 1:
            self.animationDeltaG = 0.0
            self.currentLampModel.g = readyRGB[1]
        diffB = readyRGB[2] - self.currentLampModel.b
        if abs(diffB) <= 1:
            self.animationDeltaB = 0.0
            self.currentLampModel.b = readyRGB[2]

        #If all deltas == 0.0 then animation is over
        if self.animationDeltaR == 0.0 and self.animationDeltaG == 0.0 and self.animationDeltaB == 0.0:
            self.lampIsAnimating = False

    def updateLamp(self):
        if self.lampIsAnimating:
            # Add deltas to lamp
            self.currentLampModel.r += self.animationDeltaR
            self.currentLampModel.g += self.animationDeltaG
            self.currentLampModel.b += self.animationDeltaB

            # Check if ready
            self.checkLampAnimationReady()

            # Add new lamp to controller queue
            self.lampControllerQueue.put(self.currentLampModel)

    def towerModelChanged(self, newTowerModel):
        self.oldTowerModel = self.currentTowerModel
        self.currentTowerModel = newTowerModel
        self.towerControllerQueue.put(self.currentTowerModel)
        self.startLampAnimation()

    def isTowerModelDifferent(self, newTowerModel):
        # This is kind of hard... Have to research how you calculate the size of a change from one RGB to another.

        # Calculate diff for each rgb channel
        diffR = abs(self.currentTowerModel.averageWindowRGB[0] - newTowerModel.averageWindowRGB[0])
        diffG = abs(self.currentTowerModel.averageWindowRGB[1] - newTowerModel.averageWindowRGB[1])
        diffB = abs(self.currentTowerModel.averageWindowRGB[2] - newTowerModel.averageWindowRGB[2])

        # Calculate percentage diff, check that no division by zero
        if self.currentTowerModel.averageWindowRGB[0] != 0:
            changeR = float(abs(diffR))/float(self.currentTowerModel.averageWindowRGB[0])
        else:
            changeR = float(abs(diffR))/127.5  # half of 255

        if self.currentTowerModel.averageWindowRGB[1] != 0:
            changeG = float(abs(diffG))/float(self.currentTowerModel.averageWindowRGB[1])
        else:
            changeG = float(abs(diffG))/127.5  # half of 255

        if self.currentTowerModel.averageWindowRGB[2] != 0:
            changeB = float(abs(diffB))/float(self.currentTowerModel.averageWindowRGB[2])
        else:
            changeB = float(abs(diffB))/127.5  # half of 255

        # Check if change over treshold
        isDifferent = False
        CHANGE = self.towerChangedTreshold
        if changeR > CHANGE:
            isDifferent = True
        if changeG > CHANGE:
            isDifferent = True
        if changeB > CHANGE:
            isDifferent = True

        # Print to log
        print "TowerModel difference:"
        print "Current: %s, New: %s" %(self.currentTowerModel.averageWindowRGB, newTowerModel.averageWindowRGB)
        print "diffR: %s changeR: %s, diffG: %s changeG: %s, diffB: %s changeB: %s. Treshold: %s isDifferent: %s" % (diffR, changeR, diffG, changeG, diffB, changeB, CHANGE, isDifferent)

        return isDifferent

    def downloadTowerImage(self):
        if not self.isSimulating:
            os.system("curl -o tower_temp.jpg http://89.253.86.245//axis-cgi/jpg/image.cgi?resolution=800x450")
        else:
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

        # Mode filter image
        self.image = self.image.filter(ImageFilter.ModeFilter(5))

        # Create PITowerModel and mark as changed
        towerModel = PITowerModel(self.image)

        # Check if PITowerModel changed
        if self.currentTowerModel:
            if self.isTowerModelDifferent(towerModel):
                self.towerModelChanged(towerModel)
        else:
            self.currentTowerModel = towerModel
            self.towerModelChanged(towerModel)

    def tick(self):
        if self.ticks == self.tickTowerUpdate + 60/self.updateHZ or self.ticks == 0:
            self.tickTowerUpdate = self.ticks
            self.updateTower()
        self.updateLamp()  # lamp should update as often as possible
        self.ticks += 1
        time.sleep(self.updateHZ)
        print self.ticks

    def run(self):
        while True:
            self.tick()
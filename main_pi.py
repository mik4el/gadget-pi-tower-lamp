import Queue
from controllers import PITowerController
from views import PITowerLampVisualization
import time

# Create controller queue for communication between controller and view
towerControllerQueue = Queue.Queue()
lampControllerQueue = Queue.Queue()

# Create and start controller on separate thread
controllerThread = PITowerController("tower_temp.jpg", towerControllerQueue, lampControllerQueue)
controllerThread.daemon = True
controllerThread.start()

while True:
    if not lampControllerQueue.empty():
        lamp = lampControllerQueue.get()
        print lamp.getRGB()
        time.sleep(0.1)
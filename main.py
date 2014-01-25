import Queue
from controllers import PITowerController
from views import PITowerLampVisualization

# Create controller queue for communication between controller and view
towerControllerQueue = Queue.Queue()
lampControllerQueue = Queue.Queue()

# Create and start controller on separate thread
controllerThread = PITowerController("tower_temp.jpg", towerControllerQueue, lampControllerQueue)
controllerThread.daemon = True
controllerThread.start()

# Create and start visualization view
visualization = PITowerLampVisualization(towerControllerQueue, lampControllerQueue)
visualization.startGUI()
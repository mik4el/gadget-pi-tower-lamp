import Queue
from controllers import PITowerController
from views import PITowerLampVisualization, PITowerLampRGBLED
import argparse
from time import sleep


def main():
    parser = argparse.ArgumentParser(
        description='Start PITowerLamp')
    parser.add_argument('--mode', help='Start PITowerLamp in visual, text or lamp mode')
    args = parser.parse_args()

    # Create controller queue for communication between controller and view
    towerControllerQueue = Queue.Queue()
    lampControllerQueue = Queue.Queue()

    # Create and start controller on separate thread
    controllerThread = PITowerController("tower_temp.jpg", towerControllerQueue, lampControllerQueue)
    controllerThread.daemon = True
    controllerThread.isSimulating = True
    controllerThread.start()

    if args.mode == "visual":
        # Create and start visualization view
        visualization = PITowerLampVisualization(towerControllerQueue, lampControllerQueue)
        visualization.start()

    if args.mode == "rgbled":
        # Create and start visualization view
        visualization = PITowerLampRGBLED(towerControllerQueue, lampControllerQueue)
        visualization.start()

    if args.mode == "text":
        while True:
            if not lampControllerQueue.empty():
                lamp = lampControllerQueue.get()
                print lamp.getRGB()
                sleep(0.1)

if __name__ == "__main__":
    main()
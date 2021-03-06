import queue
import argparse
from time import sleep
from controllers import PITowerController


def main():
    parser = argparse.ArgumentParser(
        description='Start PITowerLamp')
    parser.add_argument('--mode', help='Start PITowerLamp in visual, text or lamp mode')
    args = parser.parse_args()

    # Create controller queue for communication between controller and view
    towerControllerQueue = queue.Queue()
    lampControllerQueue = queue.Queue()

    # Create and start controller on separate thread
    controllerThread = PITowerController("tower_temp.jpg", towerControllerQueue, lampControllerQueue)
    controllerThread.daemon = True
    controllerThread.isSimulating = False
    controllerThread.start()

    if args.mode == "visual":
        # Create and start visualization view
        from visualization import PITowerLampVisualization
        visualization = PITowerLampVisualization(towerControllerQueue, lampControllerQueue)
        visualization.start()

    if args.mode == "rgbled":
        # Create and start visualization view
        from daemon import PITowerLampRGBLED
        daemon = PITowerLampRGBLED(towerControllerQueue, lampControllerQueue)
        daemon.start()

    if args.mode == "text":
        while True:
            if not lampControllerQueue.empty():
                lamp = lampControllerQueue.get()
                print(lamp.getRGB())
                sleep(0.1)

if __name__ == "__main__":
    main()

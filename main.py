import Queue
from controllers import PITowerController
from views import PITowerLampVisualization
import argparse
from time import sleep


def main():
    parser = argparse.ArgumentParser(
        description='Start PITowerLamp')
    parser.add_argument('--mode', help='Start PITowerLamp in visual, text or lamp mode')
    args = parser.parse_args()

    if args.mode == "test_led":
        # Blinks the led <numTimes> with <speed>

        import RPi.GPIO as GPIO  # Lazy import of GPIO library

        GPIO.setmode(GPIO.BOARD)  # Use board pin numbering
        GPIO.setup(7, GPIO.OUT)  # Setup GPIO Pin 7 to OUT

        numTimes = 10
        speed = 0.5

        for i in range(0, numTimes):
            GPIO.output(7, True)
            sleep(speed)
            GPIO.output(7, False)
            sleep(speed)
        GPIO.cleanup()

        return

    # For other modes, a towerController wil be needed

    # Create controller queue for communication between controller and view
    towerControllerQueue = Queue.Queue()
    lampControllerQueue = Queue.Queue()

    # Create and start controller on separate thread
    controllerThread = PITowerController("tower_temp.jpg", towerControllerQueue, lampControllerQueue)
    controllerThread.daemon = True
    controllerThread.start()

    if args.mode == "visual":
        # Create and start visualization view
        visualization = PITowerLampVisualization(towerControllerQueue, lampControllerQueue)
        visualization.startGUI()

    if args.mode == "text":
        while True:
            if not lampControllerQueue.empty():
                lamp = lampControllerQueue.get()
                print lamp.getRGB()
                sleep(0.1)

if __name__ == "__main__":
    main()
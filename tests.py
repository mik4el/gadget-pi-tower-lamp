import unittest
from PIL import Image
import Queue
from models import PILampModel, PITowerModel
from controllers import PITowerController
from views import PITowerLampVisualization
from helpers import hexFromRGB

TEST_IMAGE_NAME = "tower_test_01.jpg"


class TestHelperMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_hexFromRGB(self):
        RGB = (0, 0, 0)
        result = hexFromRGB(RGB)
        self.assertEqual(result, '#%02x%02x%02x' % RGB)
        self.assertEqual(result, '#000000')


class TestPILampModel(unittest.TestCase):
    def setUp(self):
        self.lampModel = PILampModel(1, 2, 3, True)

    def test_values_set(self):
        self.assertEqual(self.lampModel.r, 1)
        self.assertEqual(self.lampModel.g, 2)
        self.assertEqual(self.lampModel.b, 3)
        self.assertEqual(self.lampModel.isOn, True)

    def test_getRGB(self):
        self.assertEqual(self.lampModel.getRGB(), (1,2,3))


class TestPITowerModel(unittest.TestCase):
    def setUp(self):
        self.image = Image.open(TEST_IMAGE_NAME)
        self.towerModel = PITowerModel(self.image)
        self.pixelsInImage = self.image.load()

    def test_rgb_values_in_image(self):
        """
        Test that an image was loaded and that rgb values can be read from a pixel in the image.
        """
        # Check that no dimension in image size is zero
        self.assertNotEqual(self.image.size[0], 0)
        self.assertNotEqual(self.image.size[1], 0)

        # Check that a array of length 3 is returned for a pixel
        self.assertEqual(len(self.pixelsInImage[1, 1]), 3)

    def test_RGBForWindow(self):
        """
        Test function RGBForWindow that maps window index to pixel position and then gets RGB for that position
        """
        # Know values per window for tower_test_01
        TOWER_TEST_IMAGE_01_RGB_PER_WINDOW = [
            (116, 32, 231),
            (77, 43, 218),
            (116, 136, 235),
            (108, 115, 221),
            (169, 231, 255),
            (47, 117, 212),
            (54, 98, 203),
            (82, 78, 214),
            (101, 45, 178),
            (223, 96, 255)
        ]
        self.assertEqual(len(TOWER_TEST_IMAGE_01_RGB_PER_WINDOW), 10)
        for i in range(len(TOWER_TEST_IMAGE_01_RGB_PER_WINDOW)):
            self.assertEqual(self.towerModel.RGBForWindow(i, pixelsInImage=self.pixelsInImage), TOWER_TEST_IMAGE_01_RGB_PER_WINDOW[i])

    def test_RGBForPixel(self):
        """
        Test function RGBForPixel
        """
        result = self.towerModel.RGBForPixel(x=1, y=1, pixelsInImage=self.pixelsInImage)
        self.assertEqual(len(result), 3)
        self.assertEqual(self.pixelsInImage[1, 1], result)

    def test_RGBForAllWindows(self):
        """
        Test function RGBForAllWindows
        """
        result = self.towerModel.RGBForAllWindows(pixelsInImage=self.pixelsInImage)
        self.assertEqual(len(result), 10)
        self.assertEqual(len(result[0]), 3)

    def test_averageRGB(self):
        TEST_RGBS = [
            (1, 1, 1),
            (1, 1, 1)
        ]
        result = self.towerModel.averageRGB(TEST_RGBS)
        self.assertEqual(result, (1, 1, 1))
        TEST_RGBS = [
            (1, 1, 1)
        ]
        result = self.towerModel.averageRGB(TEST_RGBS)
        self.assertEqual(result, (1, 1, 1))
        TEST_RGBS = [
            (1, 1, 1),
            (2, 2, 2)
        ]
        result = self.towerModel.averageRGB(TEST_RGBS)
        self.assertEqual(result, (1, 1, 1))
        TEST_RGBS = [
            (1, 1, 1),
            (3, 3, 3)
        ]
        result = self.towerModel.averageRGB(TEST_RGBS)
        self.assertEqual(result, (2, 2, 2))


class TestPITowerController(unittest.TestCase):
    def setUp(self):
        self.lampQueue = Queue.Queue()
        self.towerQueue = Queue.Queue()
        self.imageName = TEST_IMAGE_NAME
        self.towerController = PITowerController(self.imageName, self.towerQueue, self.lampQueue)
        self.image = Image.open(self.imageName)
        self.towerController.currentTowerModel = PITowerModel(self.image)
        self.towerController.currentLampModel = PILampModel(0, 0, 0, True)
        self.towerController.updateHZ = 0.1

    def test_init_variables_set(self):
        self.assertEqual(self.lampQueue, self.towerController.lampControllerQueue)
        self.assertEqual(self.towerQueue, self.towerController.towerControllerQueue)
        self.assertEqual(self.imageName, self.towerController.imageName)

    def test_startLampAnimation(self):
        # Check that no input variables for animation is set
        self.assertIsNone(self.towerController.animationStartRGB)
        self.assertIsNone(self.towerController.animationEndRGB)
        self.assertEqual(self.towerController.animationSteps, 0)
        self.assertEqual(self.towerController.lampIsAnimating, False)

        self.towerController.startLampAnimation()

        # Check that real input variables for animation is set
        self.assertEqual(self.towerController.animationStartRGB, (0, 0, 0))
        self.assertEqual(self.towerController.animationEndRGB, (109, 99, 222))
        self.assertEqual(self.towerController.animationSteps, 10.0)

        #Check that output variables are correct
        self.assertEqual(self.towerController.animationDeltaR, 10.9)
        self.assertEqual(self.towerController.animationDeltaG, 9.9)
        self.assertEqual(self.towerController.animationDeltaB, 22.2)
        self.assertEqual(self.towerController.lampIsAnimating, True)

    def test_updateLamp_and_checkLampAnimationReady(self):
        # Check correct behaviour for lampIsAnimating = False and start variables
        self.assertEqual(self.towerController.lampIsAnimating, False)
        self.assertEqual(self.towerController.currentLampModel.r, 0)
        self.assertEqual(self.towerController.currentLampModel.g, 0)
        self.assertEqual(self.towerController.currentLampModel.b, 0)
        self.assertEqual(self.lampQueue.empty(), True)

        self.towerController.startLampAnimation()

        # Check correct behaviour for lampIsAnimating = True
        self.assertEqual(self.towerController.lampIsAnimating, True)

        # Check that correct deltas are set
        self.assertEqual(self.towerController.animationDeltaR, 10.9)
        self.assertEqual(self.towerController.animationDeltaG, 9.9)
        self.assertEqual(self.towerController.animationDeltaB, 22.2)

        self.assertEqual(self.towerController.currentLampModel.r, 0)
        self.assertEqual(self.towerController.currentLampModel.g, 0)
        self.assertEqual(self.towerController.currentLampModel.b, 0)

        self.towerController.updateLamp()

        self.assertEqual(self.towerController.animationDeltaR, 10.9)
        self.assertEqual(self.towerController.animationDeltaG, 9.9)
        self.assertEqual(self.towerController.animationDeltaB, 22.2)

        # Check that correct output is set after first run
        self.assertEqual(self.towerController.currentLampModel.r, 10.9)
        self.assertEqual(self.towerController.currentLampModel.g, 9.9)
        self.assertEqual(self.towerController.currentLampModel.b, 22.2)
        self.assertEqual(self.lampQueue.empty(), False)

        # Complete animation cycle
        for i in range(int(self.towerController.animationSteps-1)):
            self.towerController.updateLamp()

        # Check that correct output is set after animation cycle
        self.assertEqual(self.towerController.currentLampModel.r, 109)
        self.assertEqual(self.towerController.currentLampModel.g, 99)
        self.assertEqual(self.towerController.currentLampModel.b, 222)
        self.assertEqual(self.lampQueue.qsize(), self.towerController.animationSteps)
        self.assertEqual(self.towerController.lampIsAnimating, False)

    def test_isTowerModelDifferent(self):
        self.assertIsNotNone(self.towerController.currentTowerModel)

        sameTower = PITowerModel(self.towerController.currentTowerModel.image)
        self.assertEqual(self.towerController.isTowerModelDifferent(sameTower), False)

        # Test different tower on differing on treshold
        differentTower = PITowerModel(self.towerController.currentTowerModel.image)
        diff = self.towerController.towerChangedTreshold+0.01
        differentTower.averageWindowRGB = (float(differentTower.averageWindowRGB[0])*(1.0-diff), float(differentTower.averageWindowRGB[1])*(1.0-diff), float(differentTower.averageWindowRGB[2])*(1.0-diff))
        self.assertEqual(self.towerController.isTowerModelDifferent(differentTower), True)

        # Test different tower on differing below treshold
        differentTower = PITowerModel(self.towerController.currentTowerModel.image)
        diff = float(self.towerController.towerChangedTreshold)-0.01
        differentTower.averageWindowRGB = (float(differentTower.averageWindowRGB[0])*(1-diff), float(differentTower.averageWindowRGB[1])*(1-diff), float(differentTower.averageWindowRGB[2])*(1-diff))
        self.assertEqual(self.towerController.isTowerModelDifferent(differentTower), False)


class TestPITowerLampVisualization(unittest.TestCase):
    def setUp(self):
        self.lampQueue = Queue.Queue()
        self.towerQueue = Queue.Queue()
        self.lampVisualization = PITowerLampVisualization(self.towerQueue, self.lampQueue)

    def test_init_variables_set(self):
        self.assertEqual(self.lampQueue, self.lampVisualization.lampControllerQueue)
        self.assertEqual(self.towerQueue, self.lampVisualization.towerControllerQueue)
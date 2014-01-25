import unittest
import Image
import Queue
from models import PILampModel, PITowerModel
from controllers import PITowerController
from views import PITowerLampVisualization
from helpers import hexFromRGB


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
        TEST_IMAGE_NAME = "tower_test_01.jpg"
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
        self.imageName = "test"
        self.towerController = PITowerController(self.imageName, self.towerQueue, self.lampQueue)

    def test_init_variables_set(self):
        self.assertEqual(self.lampQueue, self.towerController.lampControllerQueue)
        self.assertEqual(self.towerQueue, self.towerController.towerControllerQueue)
        self.assertEqual(self.imageName, self.towerController.imageName)


class TestPITowerLampVisualization(unittest.TestCase):
    def setUp(self):
        self.lampQueue = Queue.Queue()
        self.towerQueue = Queue.Queue()
        self.lampVisualization = PITowerLampVisualization(self.towerQueue, self.lampQueue)

    def test_init_variables_set(self):
        self.assertEqual(self.lampQueue, self.lampVisualization.lampControllerQueue)
        self.assertEqual(self.towerQueue, self.lampVisualization.towerControllerQueue)
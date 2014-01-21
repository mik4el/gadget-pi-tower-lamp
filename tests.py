import unittest
import Image
import main


class TestRGBForPixel(unittest.TestCase):
    def setUp(self):
        TEST_IMAGE_NAME = "tower_test_01.jpg"
        self.image = Image.open(TEST_IMAGE_NAME)
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
            self.assertEqual(main.RGBForWindow(i, pixelsInImage=self.pixelsInImage), TOWER_TEST_IMAGE_01_RGB_PER_WINDOW[i])

    def test_RGBForPixel(self):
        """
        Test function RGBForPixel
        """
        result = main.RGBForPixel(x=1, y=1, pixelsInImage=self.pixelsInImage)
        self.assertEqual(len(result), 3)
        self.assertEqual(self.pixelsInImage[1, 1], result)
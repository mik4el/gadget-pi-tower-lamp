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

    def test_RGBForPixel(self):
        """
        Test function RGBForPixel
        """
        result = main.RGBForPixel(pixelsInImage=self.pixelsInImage, x=1, y=1)
        self.assertEqual(len(result), 3)
        self.assertEqual(self.pixelsInImage[1, 1], result)
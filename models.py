class PILampModel:
    def __init__(self, r, g, b, isOn):
        self.r = r
        self.g = g
        self.b = b
        self.isOn = isOn
        print "Lamp model created!"

    def getRGB(self):
        return self.r, self.g, self.b


class PITowerModel:
    def __init__(self, image):
        self.image = image
        pixelsInImage = self.image.load()
        self.allWindowsRGB = self.RGBForAllWindows(pixelsInImage)
        self.averageWindowRGB = self.averageRGB(self.allWindowsRGB)
        print "Tower model created!"

    def RGBForPixel(self, x, y, pixelsInImage):
        return pixelsInImage[x, y]

    def RGBForWindow(self, windowNumber, pixelsInImage):
        POSITION_FOR_WINDOW_NUMBER = {
            0: [440, 299],
            1: [440, 277],
            2: [440, 255],
            3: [440, 234],
            4: [440, 212],
            5: [441, 189],
            6: [441, 169],
            7: [441, 148],
            8: [441, 126],
            9: [440, 105],
        }
        x = POSITION_FOR_WINDOW_NUMBER[windowNumber][0]
        y = POSITION_FOR_WINDOW_NUMBER[windowNumber][1]
        return self.RGBForPixel(x, y, pixelsInImage)

    def RGBForAllWindows(self, pixelsInImage):
        allRGB = []
        for i in range(10):
            allRGB.append(self.RGBForWindow(i, pixelsInImage))
        return allRGB

    def averageRGB(self, arrayOfRGB):
        R = 0
        G = 0
        B = 0
        for i in range(len(arrayOfRGB)):
            R += arrayOfRGB[i][0]
            G += arrayOfRGB[i][1]
            B += arrayOfRGB[i][2]
        R /= len(arrayOfRGB)
        G /= len(arrayOfRGB)
        B /= len(arrayOfRGB)
        return R, G, B

from Tkinter import *
from PIL import Image, ImageTk
import os
import time


def RGBForPixel(x, y, pixelsInImage):
    return pixelsInImage[x, y]


def RGBForWindow(windowNumber, pixelsInImage):
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
    return RGBForPixel(x, y, pixelsInImage)


def RGBForAllWindows(pixelsInImage):
    allRGB = []
    for i in range(10):
        allRGB.append(RGBForWindow(i, pixelsInImage))
    return allRGB


def averageRGB(arrayOfRGB):
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


def hexFromRGB(RGB):
    return '#%02x%02x%02x' % RGB


def downloadTowerImage():
    os.system("curl -o tower_temp.jpg http://89.253.86.245//axis-cgi/jpg/image.cgi?resolution=800x450")


class PITowerLampVisualization:
    def __init__(self, imageName):
        #Start Tkinter
        self.root = Tk()
        self.root.title("PI Tower Lamp Visualization")

        #Load image
        self.image = None
        self.tkImage = None
        self.pixelsInImage = None

        #Draw GUI
        self.canvas = Canvas(self.root, width=1250, height=1000)
        self.canvas.pack()
        self.root.after(0, self.visualizeImage(imageName))
        self.root.mainloop()

    def visualizeImage(self, imageName):
        while(True):

            #Download new image
            downloadTowerImage()

            #Load image
            self.image = Image.open(imageName)
            self.tkImage = ImageTk.PhotoImage(self.image)
            self.pixelsInImage = self.image.load()

            #Get RGB from image
            allWindowsRGB = RGBForAllWindows(self.pixelsInImage)

            for i in range(10):
                self.canvas.create_rectangle(0, 100*i, 200, 100*(1+i), fill=str(hexFromRGB(allWindowsRGB[9-i])))

            #Draw average RGB block
            self.canvas.create_rectangle(250, 450, 450, 550, fill=hexFromRGB(averageRGB(allWindowsRGB)))
            #Draw tower visualization
            self.canvas.create_image(900, 500, image=self.tkImage)

            print "Updated!"
            self.canvas.update()

            time.sleep(5)

PITowerLampVisualization("tower_temp.jpg")

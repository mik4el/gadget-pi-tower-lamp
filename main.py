from Tkinter import *
from PIL import Image, ImageTk


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


def showVisualization(imageName):
    #Start Tkinter
    root = Tk()
    root.title = "PI Tower Lamp Visualization"

    #Load image
    image = Image.open(imageName)
    tkImage = ImageTk.PhotoImage(image)
    pixelsInImage = image.load()

    #Get RGB from image
    allWindowsRGB = RGBForAllWindows(pixelsInImage)

    #Draw GUI
    canvas = Canvas(root, width=1250, height=1000)
    canvas.pack()
    for i in range(10):
        canvas.create_rectangle(0, 100*i, 200, 100*(1+i), fill=str(hexFromRGB(allWindowsRGB[9-i])))

    #Draw average RGB block
    canvas.create_rectangle(250, 450, 450, 550, fill=hexFromRGB(averageRGB(allWindowsRGB)))
    #Draw tower visualization
    canvas.create_image(900, 500, image=tkImage)

    mainloop()

showVisualization("tower_test_01.jpg")

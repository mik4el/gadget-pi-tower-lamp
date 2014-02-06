import os
from time import sleep

print "Testing rgb led by cycling colors using pwm with delay."
iter = 0
delta = 1
pins = [4, 17, 18]  # 4=R, 17=G, 18=B
pin = 0
index = 0

colors = [(77, 43, 218),
          (116, 136, 235),
          (108, 115, 221),
          (169, 231, 255),
          (47, 117, 212),
          (54, 98, 203),
          (82, 78, 214),
          (101, 45, 178),
          (223, 96, 255)]

# Cycle array of colors every second
while True:
    try:
        print colors[index]
        os.system('echo "%d=%.2f" > /dev/pi-blaster' % (pins[0], float(colors[index][0]) / 255.0))
        os.system('echo "%d=%.2f" > /dev/pi-blaster' % (pins[1], float(colors[index][1]) / 255.0))
        os.system('echo "%d=%.2f" > /dev/pi-blaster' % (pins[2], float(colors[index][2]) / 255.0))
        index += 1
        if index == 9:
            index = 0
        sleep(1.0)  # max hz for pi-blaster pwm
    except KeyboardInterrupt:
        print "Exiting!"
        for p in pins:
            os.system('echo "%d=0" > /dev/pi-blaster' % p)
            os.system('echo "release %d" > /dev/pi-blaster' % p)
        exit()

'''
# Cycle intensities of RGB for each channel
while True:
    try:
        os.system('echo "%d=%.2f" > /dev/pi-blaster' % (pins[pin], float(iter)*0.01))
        if iter <= 1:
            delta = 1
        if iter >= 100:
            delta = -1
            os.system('echo "%d=0" > /dev/pi-blaster' % pins[pin])
            pin += 1
            if pin == 3:
                pin = 0
        iter += delta
        sleep(0.01)  # max hz for pi-blaster pwm
    except KeyboardInterrupt:
        print "Exiting!"
        for p in pins:
            os.system('echo "%d=0" > /dev/pi-blaster' % p)
            os.system('echo "release %d" > /dev/pi-blaster' % p)
        exit()
'''

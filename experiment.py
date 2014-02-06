import os
from time import sleep

print "Testing rgb led by cycling colors using pwm with delay."
iter = 0
delta = 1
pins = [4, 17, 18]
pin = 0

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
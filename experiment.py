import os
from time import sleep

print "Testing rgb led by cycling colors using pwm with delay."
iter = 0
delta = 1
while True:
    try:
        #print 'echo "4=%.2f" > /dev/pi-blaster' % (float(iter)*0.01)
        os.system('echo "4=%.2f" > /dev/pi-blaster' % (float(iter)*0.001))
        if iter <= 1:
            delta = 1
        if iter >= 100:
            delta = -1
        iter += delta
        sleep(0.01)  # max hz for pi-blaster pwm
    except KeyboardInterrupt:
        print "Exiting!"
        os.system('echo "4=0" > /dev/pi-blaster')
        os.system('echo "release 4" > /dev/pi-blaster')
        exit()
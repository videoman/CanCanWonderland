import sys
import socket
import select
import time

pole = int(sys.argv[1])
leds = 180

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5555))

def beambreak():
    ready, _, _ = select.select([s], [], [], 0)
    if ready:
        r = s.recv(100)
        cmds = ""
        while r:
            cmds += r
            if r.endswith("\n"):
                break
            r = s.recv(100)

        if not r:
            print "disconnected"
            sys.exit()

        for cmd in cmds.splitlines():
            if cmd.startswith("ball"):
                try:
                    _, ball = r[:-1].split()
                    if int(ball) == pole:
                        return True
                except ValueError:
                    pass
    return False

def setled(num, color):
    s.send("%d %d %d %d %d\n" % (pole, num, color[0], color[1], color[2]))

clear = -1
while True:
    if beambreak():
        print "hit"
        for x in xrange(leds):
            setled(x, (200, 0, x))
        clear = time.time() + 2
    elif clear > 0 and time.time() > clear:
        for x in xrange(leds):
            setled(x, (0, 0, 0))
        clear = -1

    time.sleep(.01)

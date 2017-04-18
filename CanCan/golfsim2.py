import os
import sys
import socket
import pygame
import time
import select
import atexit
import time

poles = 8
lights = 180
lightsize = 2
polespacing = 80
width = poles * polespacing * lightsize
height = lights * lightsize

leds = []
for pole in xrange(poles):
    leds.append([(0, 0, 0)] * lights)

pygame.init()
screen = pygame.display.set_mode((width, height))

def setled(pole, num, color):
    if pole < poles and num < lights:
        leds[pole][num] = color
    else:
        print "bad led", pole, num

def showpole(pole):
    for num in xrange(lights):
        sx = (pole + .5) * polespacing * lightsize
        sy = height - (num * lightsize)
        pygame.draw.rect(screen,
                         leds[pole][num],
                         (sx, sy, lightsize, lightsize))
    pygame.display.update()

# pygame bug workaround with SDL on Linux
atexit.register(os._exit, 0)

# set up our main socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('', 5555))
server.listen(5)
sockets = [server]

lastpole = -1
lastpoletime = time.time()
running = True
while running:
    # any socket activity?
    ready, _, _ = select.select(sockets, [], [], 0)
    for s in ready:
        if s == server:
            # accept new clients, add them to list
            (client, address) = s.accept()
            sockets.append(client)
        else:
            r = s.recv(100)
            cmds = ""
            while r:
                cmds += r
                if r.endswith("\n"):
                    break
                r = s.recv(100)

            if not r:
                # client EOF, stop listening
                sockets.remove(s)

            for cmd in cmds.splitlines():
                try:
                    # try to read a command
                    if cmd.startswith("show"):
                        _, pole = cmd.split()
                        showpole(int(pole))
                    else:
                        pole, num, r, g, b = cmd.split()
                        setled(int(pole), int(num), (int(r), int(g), int(b)))
                except ValueError:
                    print "got invalid", cmd
                    continue

    # pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            pole = x / (polespacing * lightsize)

            if pole != lastpole or time.time() - lastpoletime > 2:
                print "pole", pole
                lastpole = pole
                lastpoletime = time.time()

                for s in sockets:
                    if s != server:
                        s.send("ball %d\n" % pole)

    time.sleep(.01)

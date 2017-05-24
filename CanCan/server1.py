#!/usr/bin/env python

"""
An echo server that uses threads to handle multiple clients at a time.
Entering any line of input at the terminal will exit the server.
"""

import select
import socket
import sys
import threading
import random

#instead of globals maybe make a class
global ball1check, ball2check

class PatternTimer(threading.Thread):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.server = server
    def timer_start(self):
        self.threadedTimer = threading.Timer(30, self.set_pattern)
        print 'Starting PatternTimer...'
        self.threadedTimer.start()
    def set_pattern(self):
        print 'Sending pattern change to all poles'
        self.timer_start()
        self.server.set_pattern()
        print 'Restarting PatternTimer'
        return
    
class Server:
    def __init__(self):
        self.host = ''
        self.port = 50000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        try:
            option = 1
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def run(self):
        t = PatternTimer(self)
        t.timer_start()
        self.open_socket()
        input = [self.server,sys.stdin]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])
            print "server hears something is happening...\n"
            for s in inputready:
                print "someone is joining\n"
                if s == self.server:
                    # handle the server socket
                    c = Client(self.server.accept())
                    print 'Connected with ' + str(c.client) + ':' + str(c.address) + "\n"
                    c.set_server(self)
                    c.start()
                    self.threads.append(c)
                    print "\n"

                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0 
        # close all threads
        self.server.close()
        for c in self.threads:
            print c.client
            print c.address
            c.join()
    
    def hole_in_one(self):
        print " ()()()()()()()()()() \n"
        print " \n HOLE IN ONE HAPPENED \n"
        print " ()()()()()()()()()() \n"
        for c in self.threads:
            #c.client.send("0=hole_in_one")
            c.blinky()
    def set_pattern(self):
        # randomly pick 
        pattern_list = ['purple', 'updown', 'flashing', 'rainbow', 'purplerain']
        random.shuffle(pattern_list)
        ball_pattern = 'set_pattern_ball_' + pattern_list.pop()
        screensaver_pattern = 'set_pattern_screensaver_' + pattern_list.pop()

        
        for c in self.threads:
            c.set_pattern(ball_pattern)
            
        for c in self.threads:
            c.set_pattern(screensaver_pattern)


class Client(threading.Thread):
    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        
    def blinky(self):
        self.client.send("0=hole_in_one")
        print "sending hole in one message to pole\n"

    def set_pattern(self, new_pattern):
        new_pattern_message = "set_pattern 0=" + new_pattern + "%"
        self.client.send(new_pattern_message)
        print ")()()()()()()()()()\n"
        print "sending new pattern through client connection\n"
        print new_pattern_message
        print ")()()()()()()()()()\n"
        print "\n"
                        
                        
    def processMessage(self, pole, message):
        if pole > 0 and pole < 9:
            if message == "ball":
               print "ball message received from ", pole

    def set_server(self, somevariable):
        self.server = somevariable

    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size)
           
            if data:
                global ball1check, ball2check
                lhs, rhs = data.split("=", 1)
                print "data received " + data
                self.processMessage(lhs, rhs)
            else:
                self.client.close()
                running = 0

if __name__ == "__main__":
    ball1check = 0
    ball2check = 0
    s = Server()
    s.run()

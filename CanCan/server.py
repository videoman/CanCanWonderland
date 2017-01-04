#!/usr/bin/env python

"""
An echo server that uses threads to handle multiple clients at a time.
Entering any line of input at the terminal will exit the server.
"""

import select
import socket
import sys
import threading

#instead of globals maybe make a class
global ball1check, ball2check

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
            self.server.bind((self.host,self.port))
            self.server.listen(5)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def run(self):
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

class Client(threading.Thread):
    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        
    def blinky(self):
        self.client.send("0=hole_in_one")
        print "sending hole in one message to pole\n"
                        

    def set_server(self, somevariable):
        self.server = somevariable

    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size)
            if data:
                global ball1check, ball2check
                lhs, rhs = data.split("=", 1)
                rhs = rhs[:-1]
                if lhs == "1":
                    if rhs == "ball":
                        print "ball message received  from pole 1"
                        #print "lhs " + lhs
                        #print "rhs " + rhs
                        ball1check = 1
                        #triggering a pole resets all poles after it
                        ball2check = 0
                        self.client.send("1=got_ball_message")
                        sys.stdout.write("\n\n")
                    elif rhs == "idle":
                        self.client.send("0=idle")
                    else:
                        print "unknown message received "
                        print "lhs " + lhs
                        print "rhs " + rhs
                        self.client.send("1=got_unknown_message")

        
                elif lhs == "2":
                    if rhs == "ball":
                        print "ball message received from pole 2"
                        #print "lhs " + lhs
                        #print "rhs " + rhs

                        ball2check = 1
                        if ball1check == 1:
                            self.server.hole_in_one()
                            ball1check = 0
                            ball2check = 0
                        else:
                            self.client.send("0=idle")
                            print("Pole 2 got a ball but pole 1 didn't - RESETTING CHECKS")
                            ball1check = 0
                            ball2check = 0
                        sys.stdout.write("\n\n")
                    elif rhs == "idle":
                        self.client.send("2=got_idle_message")
                    else:
                        print "unknown message received "
                        print "lhs " + lhs
                        print "rhs " + rhs

                        self.client.send("2=got_unknown_message")
        
                else:
                    self.client.send(lhs)
                    self.client.send("\n you are not a number\n")
                    self.client.send("\n message ignored\n")
                    self.client.send(rhs)
                    self.client.send("\n\n")
                    self.client.send("----------------------")
                    self.client.send("\n\n")

            else:
                self.client.close()
                running = 0

if __name__ == "__main__":
    ball1check = 0
    ball2check = 0
    s = Server()
    s.run()

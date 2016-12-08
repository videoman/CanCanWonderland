#! /usr/bin/python3

"""Check for input every 0.1 seconds. Treat available input
immediately, but do something else if idle."""

import sys
import select
import time
import socket

program_id = 2
host = 'localhost'
port = 50000
size = 1024
global s
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

# files monitored for input
read_list = [sys.stdin]
# select() should wait for this many seconds for input.
# A smaller number means more cpu usage, but a greater one
# means a more noticeable delay between input becoming
# available and the program starting to work on it.
timeout = 0.1 # seconds
last_work_time = time.time()
data = "default data"

def treat_input(linein):
  global last_work_time
  global s
  print("Workin' it!", linein)
  message_to_send = str(program_id) + "=" + linein
  s.send(message_to_send)
  data = s.recv(size)
  sys.stdout.write(data)
  sys.stdout.write("\n")
  sys.stdout.write(str(program_id))
  sys.stdout.write("\n")
  sys.stdout.write("\n++++++++++++++++++++++++\n")
  time.sleep(1) # working takes time
  print('Done')
  last_work_time = time.time()

def idle_work():
  global last_work_time
  global s
  now = time.time()
  message_to_send = str(program_id) + "=" + "idle"
  s.send(message_to_send)
  data = s.recv(size)
  lhs, rhs = data.split("=", 1)
  if lhs == program_id:
    if rhs == "got_message":
        print ""
    else:            
      sys.stdout.write(str(program_id))
      sys.stdout.write(data)
      sys.stdout.write("\n----------------------------\n")
  elif lhs == "0":
    if rhs == "hole_in_one":
        print "HOLE IN ONE BITCHES!!!\n"
  # do some other stuff every 2 seconds of idleness
  if now - last_work_time > 2:
    last_work_time = now

def main_loop():
  global read_list
  # while still waiting for input on at least one file
  while read_list:
    ready = select.select(read_list, [], [], timeout)[0]
    if not ready:
      idle_work()
    else:
      for file in ready:
        line = file.readline()
        if not line: # EOF, remove file from input list
          read_list.remove(file)
        elif line.rstrip(): # optional: skipping empty lines
          treat_input(line)

try:
    main_loop()
except KeyboardInterrupt:
  pass
#!/usr/bin/env python
#----------------------------------------------------------
# hue_cycle_server.py: Send a cycle of hues over 0mq to 
# anyone who is listening.
#----------------------------------------------------------

# Comms library
import zmq

# library for color conversion
import colorsys

# library for sleeping
import time

# convenient way to make a cycle, like a list but that wraps around
from itertools import cycle

# for commandline args
import sys

# libraries for printing pretty things to the terminal
import sparkline
from termcolor import colored

def print_sparkline(r, g, b):
    # prints a sparkline, a small graph which shows the color levels of R, G, and B
    spark = sparkline.sparkify([r, g, b])#.encode('utf-8')
    r = round(r/(255/5.))
    g = round(g/(255/5.))
    b = round(b/(255/5.))
    color_code = 16 + (r * 36) + (g * 6) + b
    shape = u'\u25CF'
    print colored(spark[0], 'red'), \
          colored(spark[1], 'green'), \
          colored(spark[2], 'blue'), \
          '\x1b[38;5;%dm' % color_code, shape

def print_publish_line(r, g, b):
    # Prints a line out to the terminal, along with our sparkline
    print "\033c"
    print_sparkline(r, g, b)


# Set up our publisher.  We'll publish to anyone listening on epgm port 5556.
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.setsockopt(zmq.LINGER, 0) # discard unsent messages on close
socket.bind("epgm://10.1.10.150:5556")

# generate a cycle of N hues
n = float(sys.argv[1])
huerange = range(1, int(n))
hues = [hue/(n*1.0) for hue in huerange]
huecycle = cycle(hues)

while True:
    # grab the next hue, convert it to rgb
    hue = huecycle.next()
    rgb = colorsys.hsv_to_rgb(hue, 1, 1)
    # convert [0,1] float color values to [0,255] integer values.
    r, g, b = (int(float_value*255) for float_value in rgb)
    # set up our message packet
    # copy our chosen color across all of the unicorn leds
    pixels = [[(r, g, b)]*8]*4 
    # print to the terminal
    print_publish_line(r, g, b)
    # send the packet
    socket.send_pyobj(pixels)
    # sleep for a frame
    time.sleep(1/n)



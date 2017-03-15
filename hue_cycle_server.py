#!/usr/bin/env python
#----------------------------------------------------------
# hue_cycle_server.py: Send a cycle of hues over 0mq to 
# anyone who is listening.
#----------------------------------------------------------

import zmq
import colorsys
import random
import time
from itertools import cycle
import sys
import json
import sparkline
from termcolor import colored

def print_sparkline(r, g, b):
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

def print_publish_line(topic_name, r, g, b):
    print "\033c", "Sending on topic %s:" % topic_name
    print_sparkline(r, g, b)



context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

#generate a cycle of N hues
n = float(sys.argv[1])
huerange = range(1, int(n))
hues = [hue/(n*1.0) for hue in huerange]
huecycle = cycle(hues)
while True:
    hue = huecycle.next()
    r_float, g_float, b_float = colorsys.hsv_to_rgb(hue, 1, 1)
    r = (int(r_float*255))
    g = (int(g_float*255))
    b = (int(b_float*255))
    topic_name = "foo"
    print "\033c"
    print "Sending on topic %s:" % topic_name
    print_sparkline(r, g, b)
    data = json.dumps({"pixels": [[(r, g, b)]*8]*4})
    #print "Topic: %s Data: %s " %( topic_name, data)
    socket.send_string("%s %s" % (topic_name, data))
    time.sleep(1/n)



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
    data = json.dumps({"pixels": [[(r, g, b)]*8]*4})
    print "Topic: %s Data: %s " %( topic_name, data)
    socket.send_string("%s %s" % (topic_name, data))
    time.sleep(1/n)

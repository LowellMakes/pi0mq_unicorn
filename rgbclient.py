#! /usr/bin/env python
# -----------------------------------------------------------------------------
# rgbclient.py - subscribe to a topic on a machine that publishes an 8x4 array 
# of RGB pixel values, write them out to the unicorn PHAT
# -----------------------------------------------------------------------------

import sys
import zmq
import unicornhat as unicorn
import colorsys
import json

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect("tcp://vulpix.lowellmakes.lan:5556")

topicfilter = "foo"
socket.setsockopt_string(zmq.SUBSCRIBE, \
                         topicfilter.decode('ascii'), \
                         encoding="utf-8")

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(0.5)


while True:
    string = socket.recv_string()
    splits = string.split()
    topic = splits[0]
    data = json.loads(' '.join(string.split()[1:]))
    pixels = data["pixels"]
    unicorn.set_pixels(pixels)
    unicorn.show()
    

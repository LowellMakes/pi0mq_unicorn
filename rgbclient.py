#! /usr/bin/env python
# -----------------------------------------------------------------------------
# rgbclient.py - subscribe to a topic on a machine that publishes an 8x4 array 
# of RGB pixel values, write them out to the unicorn PHAT
# -----------------------------------------------------------------------------

import sys
import zmq
import unicornhat as unicorn
import colorsys
import msgpack

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

# Connect to a machine (presently hardcoded to Brad's laptop
socket.connect("tcp://vulpix.lowellmakes.lan:5556")

# Only listen to a particular topic
topicfilter = "blinken"
socket.setsockopt_string(zmq.SUBSCRIBE, \
                         topicfilter.decode('ascii'), \
                         encoding="utf-8")
# Set up our unicorn hat
unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(0.5)


while True:
    # receive and unpack our message
    data = socket.recv_string()
    message = msgpack.unpackb(data)
    pixels = messsage["pixels"]
    unicorn.set_pixels(pixels)
    unicorn.show()
    

#! /usr/bin/env python
# -----------------------------------------------------------------------------
# rgbclient.py - subscribe to a topic on a machine that publishes an 8x4 array 
# of RGB pixel values, write them out to the unicorn PHAT
# -----------------------------------------------------------------------------

import zmq
import unicornhat as unicorn
import colorsys

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

# Connect to a machine (presently hardcoded to Brad's laptop
socket.connect("tcp://10.1.10.150:5556")

# Set the socket to subscribe
socket.setsockopt(zmq.SUBSCRIBE, "")
# Set up our unicorn hat
unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(0.5)

while True:
    # receive and blink out our message
    pixels = socket.recv_pyobj()
    unicorn.set_pixels(pixels)
    unicorn.show()
    

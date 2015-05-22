#!/usr/bin/env python
import zmq
import sys
import time
import os

port = 2222

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:{0}".format(port))
print("Listening on {0}".format(port))
while True:
    filename = socket.recv()
    if os.path.isfile(filename):
        socket.send_json({'result' : 'success', 'file' : open(filename).read()})
    else:
        socket.send_json({'result' : 'fail', 'reason' : '{0} is not a file or doesn\'t exist'.format(filename)})

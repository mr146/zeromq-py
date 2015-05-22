#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import os
import zmq

def getFile(filename):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:2222")
    socket.send(filename)
    response = socket.recv_json()
    return response

class HttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self):
        result = getFile(self.path[1:])
        if result.get('result') == 'success':
            self.send_response(200)
            self.send_header('content-type','application/octet-stream')
            self.end_headers()
            self.wfile.write(result.get('file'))
        else:
            self.send_response(400)
            self.send_header('content-type','text/html')
            self.end_headers()
            self.wfile.write(result.get('reason'))

serv = HTTPServer(("localhost", 8080), HttpProcessor)
serv.serve_forever()

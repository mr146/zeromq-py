#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import os

def getFile(filename):
    if os.path.isfile(filename):
        return {'result' : 'success', 'file' : open(filename).read()}
    return {'result' : 'fail', 'reason' : '{0} is not a file or doesn\'t exist'.format(filename)}

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

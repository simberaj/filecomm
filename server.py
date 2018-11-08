
'''Runs an HTTP server for file exchange over a specified port.'''

import http.server
import os

import common

def allow(path, message='Requested'):
    return input(
        '{} {}, allow (y/n)? '.format(message, path)
    ).strip().upper() in ('Y', 'A')


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.lstrip('/')
        if os.path.isfile(path):
            if allow(path, message='Requested'):
                self.send_response(200)
                self.end_headers()
                with open(path, 'rb') as infile:
                    totsize = common.transfer(infile, self.wfile)
                print('Sent', path, 'to client:', totsize, 'bytes')
            else:
                self.send_error(403)
        else:
            self.send_error(404)
        
    def do_PUT(self):
        path = self.path.lstrip('/')
        if allow(path, message='Receiving'):
            contlength = int(self.headers['Content-Length'])
            print('Receiving', path, 'from client:', contlength, 'bytes')
            if os.path.isfile(path):
                print(path, 'exists, overwriting')
            with open(path, 'wb') as outfile:
                outfile.write(self.rfile.read(contlength))
            self.send_response(200)
            self.end_headers()
            print('Transfer finished')
        else:
            self.send_error(403)


if __name__ == '__main__':
    http.server.HTTPServer(('', common.PORT), Handler).serve_forever()
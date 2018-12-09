
'''Runs a HTTP client for file exchange over a specified port.'''

import argparse
import http.client
import cmd
import os

import common


class CLI(cmd.Cmd):
    intro = 'filecomm client ready'
    prompt = '> '

    def __init__(self, conn, workdir, *args, **kwargs):
        self.conn = conn
        if not os.path.isabs(workdir):
            workdir = os.path.normpath(os.path.join(os.getcwd(), workdir))
        self.workdir = workdir
        super().__init__(*args, **kwargs)

    def preloop(self):
        self.intro = 'filecomm client ready, working from ' + self.workdir

    def do_get(self, path):
        '''Get a path-specified file from server.'''
        try:
            conn.request('GET', '/' + path)
            resp = conn.getresponse()
        except (ConnectionError, http.client.HTTPException) as message:
            print(message.__class__.__name__, message)
            return
        if resp.status == 200:
            if os.path.isfile(path):
                print(path, 'exists, overwriting')
            with open(path, 'wb') as outfile:
                totsize = common.transfer(resp, outfile)
            print(totsize, 'bytes written to', path)
        else:
            print(resp.status, resp.reason)

    def do_put(self, path):
        '''Send specified file to server.'''
        try:
            with open(path, 'rb') as sendfile:
                conn.request('PUT', '/' + path, body=sendfile.read())
                resp = conn.getresponse()
        except (FileNotFoundError, ConnectionError, http.client.HTTPException) as message:
            print(message.__class__.__name__, message)
            return

    def do_exit(self, arg):
        '''Terminate the connection and exit the client.'''
        self.conn.close()
        return True


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('host', help='host server IP address')
parser.add_argument('workdir', help='working directory, default: current', default='.')


if __name__ == '__main__':
    args = parser.parse_args()
    conn = http.client.HTTPConnection(args.host, common.PORT, timeout=common.TIMEOUT)
    CLI(conn, args.workdir).cmdloop()

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import KernelscopeCategories
from sys import argv
import SocketServer
import json
import MySQLdb
import MySQLdb.cursors

db = MySQLdb.connect(host='localhost', user='root', passwd='redhat',
        db='kernelscope', cursorclass=MySQLdb.cursors.DictCursor)
class KernelscopeLoggerService(BaseHTTPRequestHandler):
    def do_POST(self):
        json_data = self.rfile.read(int(self.headers['Content-Length']))

        self.send_response(200)
        self.end_headers()

        data = json.loads(json_data)
        print(data)
        KernelscopeCategories.dump(db, data)

def run(port=80):
    server_address = ('', port)
    kscope = HTTPServer(server_address, KernelscopeLoggerService)
    print("Starting Kernelscope Logger Service")
    kscope.serve_forever()

if len(argv) > 1:
    run(port=int(argv[1]))
else:
    run()

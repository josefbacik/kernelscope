from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import KernelscopeCategories
from sys import argv
import SocketServer
import json
import MySQLdb
import MySQLdb.cursors
from os import curdir

db = MySQLdb.connect(host='localhost', user='root', passwd='redhat',
        db='kernelscope', cursorclass=MySQLdb.cursors.DictCursor)

class KernelscopeService(BaseHTTPRequestHandler):
    def _handle_api(self):
        if self.path == "/api/getcategories":
            response = KernelscopeCategories.get_categories()
            data = json.dumps(response)
            print data
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Content-Length', len(data))
            self.end_headers();
            self.wfile.write(data)
        else:
            self.send_error(404, 'File not found')

    def do_GET(self):
        if self.path.startswith("/api"):
            self._handle_api()
            return

        if self.path == "/":
            self.path = "/index.html"

        reply = False
        if self.path.endswith('.html'):
            mimetype = "text/html"
            reply = True
        elif self.path.endswith('.json'):
            mimetype = 'application/json'
            reply = True
        elif self.path.endswith('.js'):
            mimetype = 'application/javascript'
            reply = True
        elif self.path.endswith('.css'):
            mimetype = 'text/css'
            reply = True
        print self.path
        if not reply:
            self.send_response(404);
            return
        try:
            f = open(curdir + "/web" + self.path)
            self.send_response(200)
            self.send_header('Content-type', mimetype)
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        except IOError:
            self.send_error(404, 'File not found')

    def do_POST(self):
        if self.path != "/api":
            self.send_response(405, 'Cannot post to this url')
            return

        json_data = self.rfile.read(int(self.headers['Content-Length']))

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        data = json.loads(json_data)
        print(data)
        response = KernelscopeCategories.load(db, data)
        data = json.dumps(response)
        self.send_header('Content-Length', len(data))
        self.end_headers()
        self.wfile.write(data)

def run(port=80):
    server_address = ('', port)
    kscope = HTTPServer(server_address, KernelscopeService)
    print("Starting Kernelscope Service")
    kscope.serve_forever()

if len(argv) > 1:
    run(port=int(argv[1]))
else:
    run()

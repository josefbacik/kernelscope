from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import KernelscopeCategories
from sys import argv
import SocketServer
import json
from os import curdir
import argparse
from Database import Database
from datetime import datetime

db = Database()

def date_serial(obj):
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

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
        data = json.dumps(response, default=date_serial)
        self.send_header('Content-Length', len(data))
        self.end_headers()
        self.wfile.write(data)

def run(port=80):
    server_address = ('', port)
    kscope = HTTPServer(server_address, KernelscopeService)
    print("Starting Kernelscope Service")
    kscope.serve_forever()

parser = argparse.ArgumentParser(description="Start the kernelscope service")
parser.add_argument("--sqlite", help="sqlite database to use")
parser.add_argument("--mysql", help="mysql database host to use")
parser.add_argument("--dbuser", help="database username")
parser.add_argument("--dbpassword", help="database password")
parser.add_argument("--dbname", help="database name to use", default="kernelscope")
parser.add_argument("PORT", help="port number to listen on", type=int)

args = parser.parse_args()
if args.mysql:
    db.connect_mysql(args.mysql, args.dbuser, args.dbpassword, args.dbname)
elif args.sqlite:
    db.connect_sqlite(args.sqlite)
else:
    print("Must specify either a sqlite or mysql database")
    exit(1)

run(args.PORT)

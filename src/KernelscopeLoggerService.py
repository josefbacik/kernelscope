from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import KernelscopeCategories
from sys import argv
import SocketServer
import json
import argparse
from Database import Database

db = Database()

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

parser = argparse.ArgumentParser(description="Start the logger service")
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

import json
import urllib2
import socket
from datetime import datetime

class KernelscopeLogger:
    def __init__(self, url):
        self.url = url
        self.hostname = socket.gethostname()
        self.payload = {}
        self.payload['hostname'] = socket.gethostname()

    def add_entry(self, category, entry):
        if category not in self.payload:
            self.payload[category] = []
        self.payload[category].append(entry)

    def submit(self):
        if len(self.payload) == 0:
            return
        self.payload['time'] = str(datetime.now())
        self.payload['hostname'] = self.hostname

        req = urllib2.Request(self.url)
        req.add_header('Content-type', 'application/json')
        data = json.dumps(self.payload)
        req.add_header('Content-Length', len(data))
        response = urllib2.urlopen(req, data);
        self.payload = {}

if __name__ == "main":
    print("NotLikeThis")

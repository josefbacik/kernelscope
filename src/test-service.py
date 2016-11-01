import json
import urllib2

req = urllib2.Request("http://localhost:8080/api")
query = {}
query['elements'] = ['hostname', 'process', 'elapsed']
query['limit'] = 1

constraint = {}
constraint['oper'] = 'and'
constraint['conditions'] = [ { 'process': 'fsstress', 'constraint': '='} ]
query['constraints'] = [ constraint ]

categories = { 'offcputime': query }

req.add_header('Content-type', 'application/json')
data = json.dumps(categories)
req.add_header('Content-Length', len(data))
response = urllib2.urlopen(req, data)
data = json.load(response)
print data

constraint['conditions'][0]['constraint'] = "contains"
constraint['conditions'][0]['process'] = "btrfs"
req.add_header('Content-type', 'application/json')
data = json.dumps(categories)
req.add_header('Content-Length', len(data))
response = urllib2.urlopen(req, data)
data = json.load(response)
print data


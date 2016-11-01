import json
import urllib2

req = urllib2.Request("http://localhost:8080")
query = {}
query['elements'] = ['stack', 'elapsed']
#query['limit'] = 10
query['format'] = "flamegraph"

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
print json.dumps(data) 

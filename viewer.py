from os import listdir
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "Hello, World!"
        self.wfile.write(bytes(message, "utf8"))

def startServing():
    with HTTPServer(('', 8000), handler) as server:
        server.serve_forever()

def getAllJSONs():
    files = listdir('data')

    result = []
    for p in files:
        try:
            with open(f'data/{p}', 'r') as f:
                # content = ''.join(f.readlines())
                parsed = json.load(f)
                result.append(parsed)
        except:
            print(f'failed to read/parse {p}')

def generateHTML():
    pass

import json
from datetime import datetime
from os import listdir, path
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import final
import dealers

HTML_CSS = """
body {
    font-family: monospace
}

table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
    padding: 5px;
}
"""

HTML_CAR_FIELDS = [
    'scrapeTime',
    'vin',
    'dealerCategory',
    'holdStatus',
]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        self.wfile.write(bytes(generateHTML(), "utf8"))

def startServing():
    with HTTPServer(('', 8000), handler) as server:
        server.serve_forever()

def getAllCars(prefix):
    files = listdir('data')
    files.sort(key=lambda x: x[11:])

    result = []
    for fileName in files:
        if not fileName.startswith(prefix):
            continue

        filePath = f'data/{fileName}'
        try:
            with open(filePath, 'r') as f:
                parsed = json.load(f)
                result.append(parsed)
        except:
            print(f'failed to read/parse {filePath}')
    return result

def generateHTML():
    html = f'<html><style>{HTML_CSS}</style><body>'

    xsePremium = getAllCars('JTMFB')
    seWeather = getAllCars('JTMAB')

    html += generateTable(xsePremium)
    html += generateTable(seWeather)

    html += '</body></html>'
    return html

def generateTable(cars):
    table = '<table>'
    for car in cars:
        try:
            carHTML = '<tr>'
            for field in HTML_CAR_FIELDS:
                carHTML += f"<td>{car.get(field, '')}</td>"

            # Color
            carHTML += f"<td>{car.get('extColor', {}).get('marketingName')}</td>"

            # Dealer
            dealer = dealers.DEALERS.get(car.get("dealerCd", ""), {})
            carHTML += f"<td>{dealer.get('name', '')}</td>"
            carHTML += f"<td>{dealer.get('city', '')}, {dealer.get('state', '')}</td>"

            # eta
            carHTML += f"<td>{car.get('eta', {}).get('currToDate')}</td>"

            carHTML += f'<td><a href="https://guest.dealer.toyota.com/v-spec/{car.get("vin", "")}/detail">car</a></td>'
            carHTML += f'<td><a href="https://www.toyota.com/dealers/dealer/{car.get("dealerCd", "")}">dealer</a></td></tr>'
        except Exception as e:
            carHTML = str(e)
        finally:
            table += f'{carHTML}\n'

    table += '</table><br><br>'
    return table

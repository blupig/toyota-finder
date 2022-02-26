import json
import time
from os import listdir
from http.server import BaseHTTPRequestHandler, HTTPServer
import dealers
import global_vars

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

class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/':
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes(generate_html(), "utf8"))

def start_serving():
    """docstring"""
    with HTTPServer(('', 8000), HTTPHandler) as server:
        server.serve_forever()

def get_all_cars(prefix):
    """Read all cars from data dir"""
    files = listdir('data')
    files.sort(key=lambda x: -int(x[11:17]))

    result = []
    for fileName in files:
        if not fileName.startswith(prefix):
            continue

        filePath = f'data/{fileName}'
        try:
            with open(filePath, 'r', encoding='utf8') as f:
                parsed = json.load(f)
                result.append(parsed)
        except Exception:
            print(f'failed to read/parse {filePath}')
    return result

def generate_html():
    """generate_table"""
    html = f'<html><style>{HTML_CSS}</style><body>'

    sps = global_vars.total_scraped / (int(time.time()) - global_vars.start_epoch)
    html += f'Total scraped: {global_vars.total_scraped} ({sps:0.1f}/s)<br>'
    html += f'Last scraped: {global_vars.last_scraped}<br><br>'

    xse_premium = get_all_cars('JTMFB')
    se_weather = get_all_cars('JTMAB')

    html += generate_table(xse_premium)
    html += generate_table(se_weather)

    html += '</body></html>'
    return html

def generate_table(cars):
    """generate_table"""
    table = '<table>'
    for car in cars:
        try:
            car_html = '<tr>'
            for field in HTML_CAR_FIELDS:
                car_html += f"<td>{car.get(field, '')}</td>"

            # Color
            car_html += f"<td>{car.get('extColor', {}).get('marketingName')}</td>"

            # Dealer
            dealer = dealers.DEALERS.get(car.get("dealerCd", ""), {})
            car_html += f"<td>{dealer.get('name', '')}</td>"
            car_html += f"<td>{dealer.get('city', '')}, {dealer.get('state', '')}</td>"

            # eta
            car_html += f"<td>{car.get('eta', {}).get('currToDate')}</td>"

            car_html += f'<td><a href="https://guest.dealer.toyota.com/v-spec/{car.get("vin", "")}/detail">car</a></td>'
            car_html += f'<td><a href="https://www.toyota.com/dealers/dealer/{car.get("dealerCd", "")}">dealer</a></td></tr>'
        except Exception as e:
            car_html = str(e)
        finally:
            table += f'{car_html}\n'

    table += '</table><br><br>'
    return table

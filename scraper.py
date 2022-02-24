import json
import urllib.request
import time
from datetime import datetime
from urllib.error import HTTPError

def scrapeVINs(vins):
    for vin in vins:
        print(f'scraping {vin}')
        try:
            body = fetchVIN(vin)
            if len(body) > 100:
                print(f'VIN {vin} exists')

                scrapeTime = readScrapeTime(vin)
                if scrapeTime is None:
                    scrapeTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                parsed = json.loads(body)
                parsed['scrapeTime'] = scrapeTime

                saveData(vin, parsed)
        except HTTPError:
            pass

        except Exception as e:
            print(str(e))

        time.sleep(1)

def fetchVIN(vin):
    url = f'https://api.rti.toyota.com/marketplace-inventory/vehicles/{vin}?isVspec=true'
    headers = {
        'referer': 'https://guest.dealer.toyota.com/',
    }
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    return resp.read()

def readScrapeTime(vin):
    try:
        with open(f'data/{vin}.json', 'r') as f:
            parsed = json.load(f)
            return parsed.get('scrapeTime', None)
    except:
        return None

def saveData(vin, car):
    with open(f'data/{vin}.json', 'w') as f:
        json.dump(car, f)

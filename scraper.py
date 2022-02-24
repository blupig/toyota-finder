import urllib.request
import time

def scrapeVINs(vins):
    for vin in vins:
        print(f'scraping {vin}')
        try:
            body = fetchVIN(vin)
            if len(body) > 100:
                print(f'VIN {vin} exists')
                saveData(vin, body)
        except:
            pass

        time.sleep(1)

def fetchVIN(vin):
    url = f'https://api.rti.toyota.com/marketplace-inventory/vehicles/{vin}?isVspec=true'
    headers = {
        'referer': 'https://guest.dealer.toyota.com/',
    }
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    return resp.read()

def saveData(vin, content):
    with open(f'data/{vin}.json', 'wb') as f:
        f.write(content)

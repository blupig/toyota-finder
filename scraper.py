import json
import traceback
import urllib.request
import time
from datetime import datetime
from urllib.error import HTTPError
import notifier

def scrape_vins(vins):
    """Scrape all VINs provided"""
    for vin in vins:
        print(f'scraping {vin}')
        try:
            body = fetch_vin(vin)
            if len(body) > 1000:
                print(f'VIN {vin} exists')

                # Read or generate scrape_time
                scrape_time = read_scrape_time(vin)
                if scrape_time is None:
                    scrape_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # New car found
                    notifier.send_email(f'toyota-finder: {vin}', f'New VIN found: {vin}')

                # Inject scrape_time
                parsed = json.loads(body)
                parsed['scrapeTime'] = scrape_time

                save_data(vin, parsed)

        except HTTPError:
            pass
        except Exception:
            traceback.print_exc()

        time.sleep(0.5)

def fetch_vin(vin):
    """Fetch single VIN"""

    url = f'https://api.rti.toyota.com/marketplace-inventory/vehicles/{vin}?isVspec=true'
    headers = {
        'referer': 'https://guest.dealer.toyota.com/',
    }
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    return resp.read()

def read_scrape_time(vin):
    """Read scrapeTime from existing file"""
    try:
        with open(f'data/{vin}.json', 'r', encoding='utf8') as f:
            parsed = json.load(f)
            return parsed.get('scrapeTime', None)
    except:
        return None

def save_data(vin, car):
    """Save as JSON"""
    with open(f'data/{vin}.json', 'w', encoding='utf8') as f:
        json.dump(car, f)

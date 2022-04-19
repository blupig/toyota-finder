import threading
import scraper
import viewer
import vin_generator

def main():
    """Program entry"""

    t_scraper = threading.Thread(target=start_scraper)
    t_viewer = threading.Thread(target=start_viewer)

    t_scraper.start()
    t_viewer.start()
    t_scraper.join()
    t_viewer.join()

def start_viewer():
    """Start viewer (blocking)"""
    viewer.start_serving()

def start_scraper():
    """Start scraper (blocking)"""

    def infinite_scraping(vins):
        while True:
            scraper.scrape_vins(vins)

    # Scrape these ranges concurrently
    vin_ranges = [
        (vin_generator.VIN_PREFIX_XSE_PREMIUM, 80001, 90000),
        (vin_generator.VIN_PREFIX_XSE_PREMIUM, 90001, 95000),
        (vin_generator.VIN_PREFIX_XSE_PREMIUM, 95001, 99999),
        (vin_generator.VIN_PREFIX_SE_WEATHER, 80000, 99999),
    ]

    threads = []
    for j in vin_ranges:
        print('starting scraper ', j)
        vins = vin_generator.generate_vins(*j)
        thread = threading.Thread(target=infinite_scraping, args=(vins,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

main()

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

    # Scrape these ranges concurrently
    vin_ranges = [
        (vin_generator.VIN_PREFIX_XSE_PREMIUM, 80000, 82000),
        # (vin_generator.VIN_PREFIX_XSE_PREMIUM, 82001, 84000),
        # (vin_generator.VIN_PREFIX_XSE_PREMIUM, 84001, 86000),
        # (vin_generator.VIN_PREFIX_XSE_PREMIUM, 86001, 88000),
        # (vin_generator.VIN_PREFIX_XSE_PREMIUM, 88001, 90000),
        # (vin_generator.VIN_PREFIX_SE_WEATHER, 80000, 87000),
    ]

    threads = []
    for j in vin_ranges:
        print('starting scraper ', j)
        vins = vin_generator.generate_vins(*j)
        thread = threading.Thread(target=scraper.scrape_vins, args=(vins,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

main()

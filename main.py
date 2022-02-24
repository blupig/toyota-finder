import threading
import scraper
import viewer
import vin_generator

def main():
    ts = threading.Thread(target=startScraper)
    tv = threading.Thread(target=startViewer)

    ts.start()
    tv.start()

    ts.join()
    tv.join()

def startViewer():
    viewer.startServing()

def startScraper():
    vins = vin_generator.generateVINs(vin_generator.VIN_PREFIX_XSE_PREMIUM, 80260, 90000)
    scraper.scrapeVINs(vins)

main()

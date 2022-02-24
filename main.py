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
    while True:
        print('scraper started')
        vins = vin_generator.generateVINs(vin_generator.VIN_PREFIX_XSE_PREMIUM, 80000, 95000)
        scraper.scrapeVINs(vins)

        vins = vin_generator.generateVINs(vin_generator.VIN_PREFIX_SE_WEATHER, 80000, 95000)
        scraper.scrapeVINs(vins)

main()

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
    def scrapeSE():
        print('SE scraper started')
        vins = vin_generator.generateVINs(vin_generator.VIN_PREFIX_SE_WEATHER, 80000, 87000)
        scraper.scrapeVINs(vins)

    def scrapeXSE():
        print('XSE scraper started')
        vins = vin_generator.generateVINs(vin_generator.VIN_PREFIX_XSE_PREMIUM, 84000, 87000)
        scraper.scrapeVINs(vins)

    while True:
        tSE = threading.Thread(target=scrapeSE)
        tXSE = threading.Thread(target=scrapeXSE)

        tSE.start()
        tXSE.start()
        tSE.join()
        tXSE.join()

main()

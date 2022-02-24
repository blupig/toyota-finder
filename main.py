import scraper
import vin_generator

def main():
    vins = vin_generator.generateVINs(vin_generator.VIN_PREFIX_XSE_PREMIUM, 83890, 90000)
    scraper.scrapeVINs(vins)

main()

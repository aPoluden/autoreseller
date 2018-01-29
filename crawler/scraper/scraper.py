from crawler.scraper.classes.autopscrapers import AutoPScraper

class Scraper:
    '''
    Entrypoint
    '''
    def __init__(self):
        self.scraper = None

    def set_autop(self, advert_type):
        '''
        Sets PortalScraper type
        params:
            advert_type type of advertisement
        '''
        self.scraper = AutoPScraper(advert_type)

    def scrape_particular_advert(self, advert_url, path=None):
        '''
        Scrapes Portal particular adverisement URL
        returns: scraped advertisement data
        '''
        return self.scraper.scrape_particular_advert(advert_url, path)
 
    def scrape_entire_adverts(self):
        '''
        Write description
        '''
        return self.scraper.scrape_entire_adverts()

    def type(self):
        '''
        returns: Scraper instance
        '''
        return self.scraper
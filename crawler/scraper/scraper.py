from crawler.scraper.classes.autopscrapers import AutoPScraper

# Scraper description - scrape content from web page response
class Scraper:
    '''
    Entrypoint
    '''
    def __init__(self):
        self.scraper = None

    def set_autop(self, advert_type, robot_type=None):
        '''
        Sets PortalScraper type
        params:
            advert_type type of advertisement
            robot_type type of robot
        '''
        self.scraper = AutoPScraper(advert_type, robot_type)

    def scrape_particular_advert(self, advert_url, path=None):
        '''
        Scrapes Portal particular adverisement URL
        returns: scraped advertisement data
        '''
        return self.scraper.scrape_particular_advert(advert_url, path)
 
    def scrape_entire_adverts(self):
        '''
        Scrapes all adverts
        returns generator
        '''
        return self.scraper.scrape_entire_adverts()

    def type(self):
        '''
        returns: Scraper instance
        '''
        return self.scraper

    def bot(self):
        '''
        Returns scraper Robot instance
        '''
        return self.scraper.bot()
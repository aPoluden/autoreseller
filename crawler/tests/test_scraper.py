from django.test import TestCase

from crawler.scraper.scraper import Scraper
from crawler.scraper.classes.options import AdvertOptions
from crawler.scraper.classes.autopscrapers import AutoPScraper, AutoPCarScraper
from crawler.scraper.classes.models import Advertisement

# Create your tests here.
class AutoPliusScraperTest(TestCase):

    def setUp(self):
        self.scraper = Scraper()
        self.scraper.set_autop(AdvertOptions.CARS)

    def test_car_scraper_selection(self): 
        '''
        Test if correct scraper selected by provided option
        '''
        self.assertEquals(AutoPScraper, type(self.scraper.type()))

    def test_particular_advert_scrape(self):
        '''
        Tests paricular car advetisement scrape
        '''
        self.scraper.set_autop(AdvertOptions.CARS)
        # TODO FIX IT USE PYTHONPATH
        url = 'file:///home/apoluden/Programming/workspace/autoreseller/crawler/tests/bmw_advertisement.html'
        # url = 'file:///home/apoluden/Programming/workspace/reseller/scraper/tests/bmw_advertisement.html'
        scraped_advert = self.scraper.scrape_particular_advert(None, path=url)
        vehicle = scraped_advert['vehicle']
        advert = scraped_advert['advert']
        seller = scraped_advert['seller']
        self.assertEquals('+37069157207', seller['number'])
        self.assertEquals('5004458', advert['uid'])
        self.assertEquals('Panevėžys,Lietuva', advert['location'])
        self.assertEquals('10 900 €', advert['price'])
        self.assertEquals('BMW', vehicle['make'])
        self.assertEquals('520', vehicle['model'])

    def test_entire_portal_advert_scrape(self):
        '''
        Test entire portal adverisement scrape
        '''
        # TODO implement test
        pass

    def test_bad_webpage_url_or_path(self):
        '''
        Tests wrong URL or path
        '''
        wrong_path = 'file://wrong/path'
        wrong_url = 'http://wrong.url'
        scraper = AutoPCarScraper()
        self.assertIsNone(scraper.page_content(wrong_url))
        self.assertIsNone(scraper.page_content(None, wrong_path))
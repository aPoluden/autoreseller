from django.test import TestCase

import unittest, requests, urllib, os
from unittest import mock
from requests import Response

from crawler.models import WebDriverSession
from crawler.scraper.scraper import Scraper
from crawler.scraper.classes.options import AdvertOptions, Bot
from crawler.scraper.classes.autopscrapers import AutoPScraper, AutoPCarScraper
from crawler.scraper.classes.robot import DefaultRobot

# Create your tests here.
class AutoPliusScraperTest(TestCase):

    def setUp(self):
        self.scraper = Scraper()
        self.scraper.set_autop(AdvertOptions.CARS, Bot.YANDEX)

    def test_car_scraper_selection(self): 
        '''
        Test if correct scraper selected by provided option
        '''
        self.assertEquals(AutoPScraper, type(self.scraper.type()))

    def test_scraper_bot_selection(self):
        '''
        Test crawling bot selection
        '''
        self.assertIsNotNone(self.scraper.bot())
        self.assertEquals(YandexRobot, type(self.scraper.bot()))

    @mock.patch('crawler.scraper.classes.robot.DefaultRobot.visit_url')
    def test_particular_lt_advert_scrape(self, visit_url):
        '''
        Tests paricular Lithuanian car advetisement scrape
        '''
        page_path = 'file:///' + os.path.dirname(os.path.abspath(__file__)) + '/resources/bmw_new_layout.html'
        visit_url.return_value = urllib.request.urlopen(page_path).read()
        self.scraper.set_autop(AdvertOptions.CARS)
        scraped_advert = self.scraper.scrape_particular_advert('https://google.com')
        vehicle = scraped_advert['vehicle']
        advert = scraped_advert['advert']
        seller = scraped_advert['seller']
        self.assertEquals('+37061111943+37061624474', seller['number'])
        self.assertEquals('7773811', advert['uid'])
        self.assertEquals('Kretinga, Lietuva', advert['location'])
        self.assertEquals('2100€', advert['price'])
        self.assertEquals('BMW', vehicle['make'])
        self.assertEquals('318', vehicle['model'])

    @unittest.skip('Logic not implemented')
    def test_particular_en_advert_scrape(self):
        '''
        Tests particular English car advertisement scrape 
        ''' 
        # TODO FIX IT USE PYTHONPATH
        url = 'file:///' + os.path.dirname(os.path.abspath(__file__)) + '/resources/mb_advertisement_eng.html'
        scraped_advert = self.scraper.scrape_particular_advert(None, path=url)
        vehicle = scraped_advert['vehicle']
        advert = scraped_advert['advert']
        seller = scraped_advert['seller']
        self.assertEquals('+37060546054', seller['number'])
        self.assertEquals('6640147', advert['uid'])
        self.assertEquals('Kaunas,Lietuva', advert['location'])
        self.assertEquals('4 900 €', advert['price'])
        self.assertEquals('Mercedes-Benz', vehicle['make'])
        self.assertEquals('E240', vehicle['model'])

    @mock.patch('crawler.scraper.classes.robot.DefaultRobot.visit_url')
    def test_particular_lt_advert_special_price_occasion(self, visit_url):
        '''
        Tests advert mixed price scrapes
        '''
        page_path = 'file:///home/apoluden/Programming/workspace/autoreseller/crawler/tests/resources/bmw-m6-4-4-l-sedanas-2015-benzinas-6698601.html'
        visit_url.return_value = urllib.request.urlopen(page_path).read()
        self.scraper.set_autop(AdvertOptions.CARS)
        scraped_advert = self.scraper.scrape_particular_advert('https://google.com')
        advert = scraped_advert['advert']
        price = advert['price']
        self.assertEquals('33 000 €', advert['price'])

    @mock.patch('crawler.scraper.classes.robot.DefaultRobot.visit_url')
    def test_particular_lt_advert_phone_number_occasion(self, visit_url):
        '''
        Test phone number assignement special occasion
        '''
        page_path = 'file:///home/apoluden/Programming/workspace/autoreseller/crawler/tests/resources/volvo-xc60-2-4-l-visureigis-2014-dyzelinas-6604091.html'
        visit_url.return_value = urllib.request.urlopen(page_path).read()
        self.scraper.set_autop(AdvertOptions.CARS)
        scraped_advert = self.scraper.scrape_particular_advert('https://google.com')
        seller = scraped_advert['seller']
        self.assertEquals('+37069994997', seller['number'])
    
    @unittest.skip('Not implemented yet')
    def test_entire_portal_advert_scrape(self):
        '''
        Test entire portal adverisement scrape
        '''
        # TODO implement test
        pass

    @mock.patch('crawler.scraper.classes.autopscrapers.AutoPCarScraper.get_car_advert_data')
    @mock.patch('crawler.scraper.classes.robot.DefaultRobot.visit_url')
    def test_instant_advert_scrape_single_page(self, visit_url, get_data):
        '''
        Tests instant advert scraping on single page
        '''
        cars = []
        url = 'file:///' + os.path.dirname(os.path.abspath(__file__)) + '/resources/instant_adverts_new_layout.html'
        crawler = AutoPCarScraper()
        visit_url.return_value = urllib.request.urlopen(url).read()
        get_data.return_value = 'data'
        car = crawler.get_instant_car_advert_data()
        cars.append(next(car))
        cars.append(next(car))
        cars.append(next(car))
        cars.append(next(car))
        self.assertEquals(4, len(cars))
        self.assertIsNone(cars[3])
    
    def test_instant_advert_scrape_multiple_pages(self):
        '''
        Tests instant/new advert scraping on multiple pages
        # TODO implement
        '''
        scraper = AutoPCarScraper()

    @mock.patch('crawler.scraper.classes.robot.DefaultRobot.fake_instant_advert_session')
    @mock.patch('crawler.scraper.classes.robot.DefaultRobot.visit_url')
    def test_no_instant_adverts_to_scrape(self, visit_url, init_session):
        '''
        Tests if no instant/new available to scrape
        '''
        scraper = AutoPCarScraper()
        page_path = 'file:///home/apoluden/Programming/workspace/autoreseller/crawler/tests/resources/no_new_car_adverts.html'
        visit_url.return_value = urllib.request.urlopen(page_path).read()
        init_session.return_value = 'any_url'
        gen = scraper.get_instant_car_advert_data()
        self.assertIsNone(next(gen))
        
    @unittest.skip('Outdated')
    def test_bad_webpage_url_or_path(self):
        '''
        Tests wrong URL or path
        '''
        wrong_path = 'file://wrong/path'
        wrong_url = 'http://wrong.url'
        scraper = AutoPCarScraper()
        self.assertIsNone(scraper.page_content(wrong_url))
        self.assertIsNone(scraper.page_content(None, wrong_path))

    @mock.patch('crawler.scraper.classes.robot.DefaultRobot.visit_url')
    def test_advert_with_mixed_deffect_value(self, visit_url): 
        '''
        Test when advertisement deffect field has additional image
        '''
        scraper = AutoPCarScraper()
        page_path = 'file:///home/apoluden/Programming/workspace/autoreseller/crawler/tests/resources/toyotaWithBadDeffect.html'
        visit_url.return_value = urllib.request.urlopen(page_path).read()
        scraped_advert = scraper.get_car_advert_data('https://google.com')

class RobotsTest(TestCase): 

    def setUp(self):
        pass

    def test_browser_session_init(self):
        '''
            Test init browser session initialization
        '''
        robot = DefaultRobot()
        content = robot.get_instant_adverts_page_content()
        robot.close_session()
        number = WebDriverSession.objects.all().count()
        self.assertEquals(0, number)
        self.assertTrue('html' in content)
        
    def test_browser_session_reatach(self):
        '''
            Test reataching to existing browser session
        '''
        robot = DefaultRobot()
        # Initilize session first time with different robot
        robot.get_instant_adverts_page_content()
        anotherRobot = DefaultRobot()
        content = anotherRobot.get_instant_adverts_page_content()
        anotherRobot.close_session()
        number = WebDriverSession.objects.all().count()
        self.assertEquals(0, number)
        self.assertTrue('html' in content)
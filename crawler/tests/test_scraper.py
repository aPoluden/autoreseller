from django.test import TestCase

import unittest, requests, urllib
from unittest import mock
from requests import Response

from crawler.scraper.scraper import Scraper
from crawler.scraper.classes.options import AdvertOptions, Bot
from crawler.scraper.classes.autopscrapers import AutoPScraper, AutoPCarScraper
from crawler.scraper.classes.robot import YandexRobot, DefaultRobot

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
        page_path = 'file:///home/apoluden/Programming/workspace/autoreseller/crawler/tests/resources/bmw_advertisement.html'
        visit_url.return_value = urllib.request.urlopen(page_path).read()
        self.scraper.set_autop(AdvertOptions.CARS)
        scraped_advert = self.scraper.scrape_particular_advert('https://google.com')
        vehicle = scraped_advert['vehicle']
        advert = scraped_advert['advert']
        seller = scraped_advert['seller']
        self.assertEquals('+37069157207', seller['number'])
        self.assertEquals('5004458', advert['uid'])
        self.assertEquals('Panevėžys,Lietuva', advert['location'])
        self.assertEquals('10 900 €', advert['price'])
        self.assertEquals('BMW', vehicle['make'])
        self.assertEquals('520', vehicle['model'])

    @unittest.skip('Logic not implemented')
    def test_particular_en_advert_scrape(self):
        '''
        Tests particular English car advertisement scrape 
        ''' 
        # TODO FIX IT USE PYTHONPATH
        url = 'file:///home/apoluden/Programming/workspace/autoreseller/crawler/tests/mb_advertisement_eng.html'
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

    @mock.patch('crawler.scraper.classes.robot.DefaultRobot.fake_instant_advert_session')
    @mock.patch('crawler.scraper.classes.autopscrapers.AutoPCarScraper.get_car_advert_data')
    @mock.patch('crawler.scraper.classes.robot.DefaultRobot.visit_url')
    def test_instant_advert_scrape_single_page(self, visit_url, get_data, init):
        '''
        Tests instant advert scraping on single page
        '''
        cars = []
        page_path = 'file:///home/apoluden/Programming/workspace/autoreseller/crawler/tests/resources/instant_adverts_single_page.html'
        crawler = AutoPCarScraper()
        visit_url.return_value = urllib.request.urlopen(page_path).read()
        get_data.return_value = 'data'
        init.return_value = 'url'
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
        self.yndx_bot = YandexRobot()
        self.dflt_bot = DefaultRobot()
        self.user_agnt_yandex = 'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)'
        self.user_agnt_dflt = 'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'
    
    def test_bot_user_agent(self):
        self.assertEquals(self.user_agnt_yandex, self.yndx_bot.get_user_agent())
        self.assertEquals(self.user_agnt_dflt, self.dflt_bot.get_user_agent())

    def test_response_yandex_robot(self):
        content = self.yndx_bot.visit_url('https://google.com')
        self.assertIsNotNone(content)

    def test_request_exception_abilities(self):
        content = self.yndx_bot.visit_url('http://test.test')
        self.assertIsNone(content)

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
        page_path = 'file:///home/apoluden/Programming/workspace/autoreseller/crawler/tests/bmw_advertisement.html'
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

    @unittest.skip('Not finished')
    def test_particular_lt_advert_scrape_en(self): 
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

    @unittest.skip('Not implemented yet')
    def test_entire_portal_advert_scrape(self):
        '''
        Test entire portal adverisement scrape
        '''
        # TODO implement test
        pass

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

class RobotsTest(TestCase): 

    def setUp(self):
        self.yndx_bot = YandexRobot()
        self.dflt_bot = DefaultRobot()
        self.user_agnt_yandex = 'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)'
        self.user_agnt_dflt = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    
    def test_bot_user_agent(self):
        self.assertEquals(self.user_agnt_yandex, self.yndx_bot.get_user_agent())
        self.assertEquals(self.user_agnt_dflt, self.dflt_bot.get_user_agent())

    def test_response_yandex_robot(self):
        content = self.yndx_bot.visit_url('https://google.com')
        self.assertIsNotNone(content)

    def test_request_exception_abilities(self):
        content = self.yndx_bot.visit_url('http://test.test')
        self.assertIsNone(content)
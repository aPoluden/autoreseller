from django.test import TestCase

import unittest
from unittest import mock

from crawler.tasks import daily_advert_check_task
from crawler.models import Advertisement, Seller, Vehicle

class CrawlerTaskTest(TestCase):

    def setUp(self):
        self.advert_phone = '+37069157207'
        self.advert_data = {
          'vehicle': {
            'Durų skaičius': '4/5',
            'Saugumas': 'SRS oro pagalvės',
            'Eksterjeras': 'Lengvojo lydinio ratlankiai,"Metallic" dažai',
            'Defektai': 'Be defektų',
            'Euro standartas': 'Euro 5',
            'Ratlankių skersmuo': 'R19',
            'Kėbulo tipas': 'Universalas',
            'Pavarų dėžė': 'Mechaninė',
            'Spalva': 'Juoda',
            'Sėdimų vietų skaičius': '5',
            'Vairo padėtis': 'Kairėje',
            'Tech. apžiūra iki': '2019-11',
            'Kuro tipas': 'Dyzelinas',
            'Kaina Lietuvoje': '10 900 €',
            'Vidutinės': '9.00',
            'Varantieji ratai': 'Galiniai',
            'Nuosava masė, kg': '1785',
            'Elektronika': 'El. valdomi langai,Autopilotas',
            'Variklis': '1995 cm³, 183 AG (135kW)',
            'Klimato valdymas': 'Klimato kontrolė',
            'Pirmosios registracijos šalis': 'Prancūzija',
            'VIN patikra': 'Patikrink šį automobilį',
            'Audio/video įranga': 'Navigacija/GPS',
            'Salonas': 'Odinis salonas,Vairo stiprintuvas',
            'Kiti ypatumai': 'Serviso knygelė',
            'Kaina eksportui': '10 900 €',
            'Rida': '175 796 km',
            'Pagaminimo data': '2010-12',
            'make' : 'BMW', 
            'model' : '520'
          },
          'seller': {
            'number': self.advert_phone
          },
          'advert': {
            'comment': '\n                Pervaryta is prancuzijos, as pirmas savininkas lietuvoje. Neseniai pakeisti tepalai ,filtrai. Vedama servizo knygele,du pulteliai plius ziemines ir vasarines padanos su ratlankiais bmw.Nusipirkus automobilį, nereikės papildomų investicijų.\n                            ',
            'location': 'Panevėžys,Lietuva',
            'uid': '5004458',
            'price': '10 900 €'
          }
        }

    @mock.patch('crawler.tasks.crawl_delay', 0)
    @mock.patch('crawler.scraper.scraper.Scraper.scrape_entire_adverts')
    def test_new_advertisement_creation(self, scrape_method):
        '''
        Checks totaly new records(Seller, Advertisement, Vehicle)
        creation wich doesn't exits in DB
        '''
        # imitates generator
        scrape_method.return_value = iter([self.advert_data])
        daily_advert_check_task()
        self.assertEquals(1, Advertisement.objects.all().count())
        self.assertEquals(1, Seller.objects.all().count())
        self.assertEquals(1, Vehicle.objects.all().count())

    @mock.patch('crawler.tasks.crawl_delay', 0)
    @mock.patch('crawler.scraper.scraper.Scraper.scrape_entire_adverts')
    def test_new_advertisement_creation_when_seller_exists(self, scrape_method):
        seller = Seller.objects.create(phone_number=self.advert_phone)
        # imitates generator
        scrape_method.return_value = iter([self.advert_data])
        daily_advert_check_task()
        advert = Advertisement.objects.all()[0]
        self.assertEquals(seller, advert.seller)
        self.assertEquals(1, Vehicle.objects.all().count())

    @mock.patch('crawler.tasks.crawl_delay', 0)
    @mock.patch('crawler.scraper.scraper.Scraper.scrape_entire_adverts')
    def test_when_no_advertisements_data(self, scrape_method):
        '''
        Test when no advertisements has been crawled, 
        or no advertisements left to scrape
        '''
        scrape_method.return_value = iter([None])
        daily_advert_check_task()
        self.assertEquals(0, Seller.objects.all().count())
        self.assertEquals(0, Advertisement.objects.all().count())
        self.assertEquals(0, Vehicle.objects.all().count())

# TODO test advertisement UPDATE
# TODO scraping agent
# TODO session ID 
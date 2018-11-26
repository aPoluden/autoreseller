from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction
from django.core import mail
from django.test.utils import override_settings

import datetime, dateparser

from crawler.models import Seller, Advertisement, Vehicle, Subscriber, WebDriverSession
from crawler.scraper.classes.options import Portals

class SellerTest(TestCase):

    def setUp(self):
       self.phone_number1 = '66666666'

    def test_uniq_seller_creation(self):
        '''
        Test if seller is uniq by phone number
        '''
        Seller.objects.create(phone_number=self.phone_number1)     
        with self.assertRaises(IntegrityError): 
            with transaction.atomic():
                Seller.objects.create(phone_number=self.phone_number1)
        self.assertEquals(1, Seller.objects.all().count())

class AdvertisementTest(TestCase):

    def setUp(self):
        self.advert = Advertisement()
        self.seller = Seller.objects.create(phone_number='66666666')

    def test_advert_creation_without_attibutes(self): 
        '''
        Test Advertisment create when attributes is not assigned
        '''
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.advert.save()

    def test_advert_created_at_assignement(self):
        '''
        Test creation timestamp assignement
        '''
        self.assertIsNotNone(self.advert.created_at)

    def test_advert_creation(self): 
        '''
        Test simple advertisement creation
        '''
        self.advert.seller = self.seller
        self.advert.uid = 10
        self.advert.save()
        self.assertIsNotNone(self.advert.id)

class VehicleTest(TestCase):

    def setUp(self):
        self.vehicle = Vehicle()
        self.seller = Seller.objects.create(phone_number='')
        self.advert = Advertisement.objects.create(seller=self.seller, uid=10)
        self.make = 'Nissan'
        self.model = 'Almera'
        self.odometr = 10
        self.deffects = 'unsellable'
        self.engine = 'turbo'
        self.transmission = 'mech'
        self.fuel = 'pepsi'
        self.year = '2000'
        self.ti = '2000-01'
        self.converted_year = dateparser.parse(self.year)
        self.converted_ti = dateparser.parse(self.ti)
        self.vhcl_dict = { 'make': self.make,
                        'model': self.model, 
                        'Rida' : self.odometr, 
                        'Defektai' : self.deffects, 
                        'Variklis' : self.engine,
                        'Pavarų dėžė' : self.transmission,
                        'Kuro tipas' : self.fuel, 
                        'Pagaminimo data' : self.year,
                        'Tech. apžiūra iki' : self.ti}

    def test_vehicle_creation(self):
        '''
        Test simple vehicle creation
        '''
        self.vehicle.seller = self.seller
        self.vehicle.advertisement = self.advert
        self.vehicle.make = 'Nissan'
        self.vehicle.model = 'Almera'
        self.vehicle.year = self.converted_year
        self.vehicle.save()
        self.assertIsNotNone(self.vehicle.id)

    def test_vehicle_param_merge_with_all_params(self):
        '''
        Test vehicle field merge with all available dict params
        '''
        vhcl = Vehicle.merge_params(self.vhcl_dict)
        self.assertEquals(self.make, vhcl.make)
        self.assertEquals(self.model, vhcl.model)
        self.assertEquals(self.odometr, vhcl.odometr_value)
        self.assertEquals(self.deffects, vhcl.deffects)
        self.assertEquals(self.engine, vhcl.engine)
        self.assertEquals(self.transmission, vhcl.transmission)
        self.assertEquals(self.fuel, vhcl.fuel)
        self.assertEquals(self.converted_year, vhcl.year)
        self.assertEquals(self.converted_ti, vhcl.technical_inspection)

    def test_vehicle_param_merge_with_not_existing_keys(self): 
        '''
        Test vehicle field merge when not all fields provided
        '''
        pop_dict = self.vhcl_dict
        pop_dict.pop('Variklis' ,None)
        pop_dict.pop('Rida', None)
        vhcl = Vehicle.merge_params(pop_dict)
        self.assertEquals(self.make, vhcl.make)
        self.assertEquals(self.model, vhcl.model)
        self.assertEquals(self.deffects, vhcl.deffects)
        self.assertEquals(self.transmission, vhcl.transmission)
        self.assertEquals(self.fuel, vhcl.fuel)
        self.assertEquals(self.converted_year, vhcl.year)
        self.assertEquals(self.converted_ti, vhcl.technical_inspection)

class SubscriberTest(TestCase):

    def setUp(self):
        self.email = 'test@email.com'
        self.subscriber0 = Subscriber.objects.create(name='Test0', email=self.email)
        self.subscriber1 = Subscriber.objects.create(name='Test0', subscribed=False)

    def testGetSubscribedEmails(self):
        '''
        Tests email fetch of subscribed users
        '''
        email_list = Subscriber.get_subscribed_emails()
        self.assertEquals(len(email_list), 1)
        self.assertEquals(email_list[0], self.email)

    def testEmailSendingToSubscribedUsers(self):
        '''
        Tests email sending to subscribed users
        '''
        message = 'Hello World'
        Subscriber.notify_all(message)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].body, message)
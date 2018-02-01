from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction

import datetime

from crawler.models import Seller, Advertisement, Vehicle

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
        self.year = '2000-01'
        self.ti = '2000-01'
        self.converted_year = datetime.datetime.strptime(self.year, '%Y-%m').date()
        self.converted_ti = datetime.datetime.strptime(self.ti, '%Y-%m').date()
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
        self.vehicle.save()
        self.assertIsNotNone(self.vehicle.id)

    def test_vehicle_param_merge(self):
        '''
        Test vehicle field merge with dict params
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
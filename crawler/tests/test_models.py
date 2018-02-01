from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction

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
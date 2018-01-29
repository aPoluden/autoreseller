from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction

from crawler.models import Seller, Advertisement

class SellerTest(TestCase):

    def setUp(self):
       self.phone_number1 = '67309726'

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
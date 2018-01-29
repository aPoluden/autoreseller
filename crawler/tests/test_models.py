from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction

from crawler.models import Seller

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
                Seller.objects.create(phone_number=self.phone_number1)s
        self.assertEquals(1, Seller.objects.all().count())


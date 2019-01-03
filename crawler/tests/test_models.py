from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction
from django.core import mail
from django.test.utils import override_settings

import datetime, dateparser

from crawler.models import Seller, Advertisement, Vehicle, Subscriber, WebDriverSession, SearchCriteria
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
        self.seller = Seller.objects.create(phone_number='123')
        self.subscriber0 = Subscriber.objects.create(name='Test0', email=self.email, role='ADMIN')
        self.subscriber1 = Subscriber.objects.create(name='Test0', subscribed=False)
        self.criteria = SearchCriteria.objects.create(make='audi',
            model='sto',
            city='Mars',
            fuel='Dyzelinas',
            subscriber= self.subscriber0)
        self.advertisement = Advertisement.objects.create(
            url = "http://autoplius.lt",
            location = "Mars",
            uid = 1000,
            price = '1000 eu', 
            seller = self.seller)
        self.vehicle = Vehicle.objects.create(
            make = "foo",
            model = "bar",
            fuel = 'Dyzelinas',
            seller = self.seller,
            year = dateparser.parse('2000-02-01'),
            advertisement = self.advertisement)
        self.data = [{
            "seller" : Seller.objects.all()[0], 
            "advert" : Advertisement.objects.all()[0],
            "vehicle" : Vehicle.objects.all()[0]
        }]

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
    
    def testSubscriberNotificationSingleCriteriaHasMatches(self): 
        # validations
        criteria = SearchCriteria.objects.create(make='foo',
                                                 model='bar',
                                                 city='Mars',
                                                 subscriber= self.subscriber0)
        self.subscriber0.notify_instant_adverts(self.data)
        self.assertEqual(len(mail.outbox), 1)
        # message body rewied manually 

    def testSubscriberNotificationSingleCriteriaNoMatches(self):
        self.subscriber0.notify_instant_adverts(self.data)
        self.assertEqual(len(mail.outbox), 0)
        
    def testSubscriberNotificationMultipleCriteriaMatch(self):
        SearchCriteria.objects.create(
            fuel='Dyzelinas', 
            subscriber= self.subscriber0)
        SearchCriteria.objects.create(
            fuel='Dyzelinas', 
            subscriber= self.subscriber0)    
        self.subscriber0.notify_instant_adverts(self.data)
        import ipdb; ipdb.set_trace()
        self.assertEqual(len(mail.outbox), 1)
        # message body rewied manually 

    def testSubscriberNotificationByYearRange(self):
        criteria0 = SearchCriteria.objects.create(
            year_from = dateparser.parse('2000-01-01'), 
            subscriber= self.subscriber0)
        criteria1 = SearchCriteria.objects.create(
            year_to = dateparser.parse('2000-03-01'), 
            subscriber= self.subscriber0)
        criteria2 = SearchCriteria.objects.create(
            year_from = dateparser.parse('2000-01-01'),
            year_to = dateparser.parse('2000-03-01'), 
            subscriber= self.subscriber0)
        self.subscriber0.notify_instant_adverts(self.data)
        self.assertEqual(len(mail.outbox), 1)
        # message body rewied manually 

class TestSearchCriteria(TestCase):

    def setUp(self):
        self.subscriber = Subscriber.objects.create(
            name='Test0',
            email='test@email.com')
        self.criteria = SearchCriteria.objects.create(make='foo',
                                                    model='bar',
                                                    city='Mars',
                                                    fuel='Dyzelinas',
                                                    subscriber= self.subscriber)
        self.seller = Seller.objects.create(phone_number='123')
        self.advertisement = Advertisement.objects.create(
            url = "http://autoplius.lt",
            location = "Mars",
            uid = 1000, 
            seller = self.seller)
        self.vehicle = Vehicle.objects.create(
            make = "foo",
            model = "bar",
            fuel = 'Dyzelinas',
            seller = self.seller,
            year = dateparser.parse('2000-02-01'),
            advertisement = self.advertisement)
        self.data = [{
            "seller" : Seller.objects.all()[0], 
            "advert" : Advertisement.objects.all()[0],
            "vehicle" : Vehicle.objects.all()[0]
        }]

    def testCityValid(self):
        '''
            Test search criteria city match 
        '''
        filtered_data = self.criteria._filter_cities(self.data)
        self.assertEquals(len(filtered_data), 1)
        self.assertIsNotNone(filtered_data[0]['seller'])
        self.assertIsNotNone(filtered_data[0]['advert'])
        self.assertIsNotNone(filtered_data[0]['vehicle'])
    
    def testCityInvalid(self):
        '''
            Test search criteria city dismatch
        '''
        self.criteria.city = "Other"
        filtered_data = self.criteria._filter_cities(self.data)
        self.assertEquals(len(filtered_data), 0)
    
    def testCityNotSet(self):
        '''
            Test search criteria city not set
        '''
        self.criteria.city = None
        filtered_data = self.criteria._filter_cities(self.data)
        self.assertEquals(len(filtered_data), 1)
        self.assertIsNotNone(filtered_data[0]['seller'])
        self.assertIsNotNone(filtered_data[0]['advert'])
        self.assertIsNotNone(filtered_data[0]['vehicle'])
    
    def testMakeValid(self):
        '''
            Test search criteria vehicle make match 
        '''
        filtered_data = self.criteria._filter_make(self.data)
        self.assertEquals(len(filtered_data), 1)
        self.assertIsNotNone(filtered_data[0]['seller'])
        self.assertIsNotNone(filtered_data[0]['advert'])
        self.assertIsNotNone(filtered_data[0]['vehicle'])
    
    def testMakeNotSet(self): 
        '''
            Test search criteria make not sets
        '''
        self.criteria.make = None
        filtered_data = self.criteria._filter_make(self.data)
        self.assertEquals(len(filtered_data), 1)
        self.assertIsNotNone(filtered_data[0]['seller'])
        self.assertIsNotNone(filtered_data[0]['advert'])
        self.assertIsNotNone(filtered_data[0]['vehicle'])
    
    def testMakeInvalid(self):
        '''
            Test search criteria make dismatch
        '''
        self.criteria.make = 'other'
        filtered_data = self.criteria._filter_make(self.data)
        self.assertEquals(len(filtered_data), 0)
    
    def testModelValid(self):
        '''
            Test search criteria vehicle make match 
        '''
        filtered_data = self.criteria._filter_model(self.data)
        self.assertEquals(len(filtered_data), 1)
        self.assertIsNotNone(filtered_data[0]['seller'])
        self.assertIsNotNone(filtered_data[0]['advert'])
        self.assertIsNotNone(filtered_data[0]['vehicle'])
    
    def testModelNotSet(self): 
        '''
            Test search criteria make not sets
        '''
        self.criteria.model = None
        filtered_data = self.criteria._filter_model(self.data)
        self.assertEquals(len(filtered_data), 1)
        self.assertIsNotNone(filtered_data[0]['seller'])
        self.assertIsNotNone(filtered_data[0]['advert'])
        self.assertIsNotNone(filtered_data[0]['vehicle'])
    
    def testModelInvalid(self):
        '''
            Test search criteria make dismatch
        '''
        self.criteria.model = 'other'
        filtered_data = self.criteria._filter_model(self.data)
        self.assertEquals(len(filtered_data), 0)

    def testYearFromSet(self):
        '''
            Test search criteria by year from
        '''
        self.criteria.year_from = datetime.date(2000, 1, 1)
        filtered_data = self.criteria._filter_year_range(self.data)
        self.assertEquals(len(filtered_data), 1)
        self.assertIsNotNone(filtered_data[0]['seller'])
        self.assertIsNotNone(filtered_data[0]['advert'])
        self.assertIsNotNone(filtered_data[0]['vehicle'])
    
    def testYearToSet(self):
        '''
            Test search criteria by year to
        '''
        self.criteria.year_to = datetime.date(2000, 2, 1)
        filtered_data = self.criteria._filter_year_range(self.data)
        self.assertEquals(len(filtered_data), 1)
        self.assertIsNotNone(filtered_data[0]['seller'])
        self.assertIsNotNone(filtered_data[0]['advert'])
        self.assertIsNotNone(filtered_data[0]['vehicle'])
    
    def testYearRangeSet(self):
        '''
            Test search criteria year range
        '''
        self.criteria.year_to = datetime.date(2000, 2, 1)
        self.criteria.year_from = datetime.date(1999, 2, 1)
        filtered_data = self.criteria._filter_year_range(self.data)
        self.assertEquals(len(filtered_data), 1)
        self.assertIsNotNone(filtered_data[0]['seller'])
        self.assertIsNotNone(filtered_data[0]['advert'])
        self.assertIsNotNone(filtered_data[0]['vehicle'])
    
    def testFuelValid(self):
        '''
            Test search criteria vehicle make match 
        '''
        filtered_data = self.criteria._filter_fuel(self.data)
        self.assertEquals(len(filtered_data), 1)
        self.assertIsNotNone(filtered_data[0]['seller'])
        self.assertIsNotNone(filtered_data[0]['advert'])
        self.assertIsNotNone(filtered_data[0]['vehicle'])
    
    def testFuelNotSet(self):
        '''
            Test search criteria make not sets
        '''
        self.criteria.fuel = None
        filtered_data = self.criteria._filter_model(self.data)
        self.assertEquals(len(filtered_data), 1)
        self.assertIsNotNone(filtered_data[0]['seller'])
        self.assertIsNotNone(filtered_data[0]['advert'])
        self.assertIsNotNone(filtered_data[0]['vehicle'])
    
    def testFuellInvalid(self):
        '''
            Test search criteria make dismatch
        '''
        self.criteria.fuel = 'other'
        filtered_data = self.criteria._filter_fuel(self.data)
        self.assertEquals(len(filtered_data), 0)

    def testAllCriteriaArgsSet(self): 
        self.criteria.year_to = datetime.date(2001, 2, 1)
        self.criteria.year_from = datetime.date(1999, 2, 1)
        filtered_data = self.criteria.filter_data(self.data)
        self.assertEquals(len(filtered_data), 1)
        self.assertIsNotNone(filtered_data[0]['seller'])
        self.assertIsNotNone(filtered_data[0]['advert'])
        self.assertIsNotNone(filtered_data[0]['vehicle'])
    
    def testMercedesBenzSeries(self):
        # C klass
        advertisement = Advertisement.objects.create(
            location = "Mars",
            uid = 1002, 
            seller = self.seller)
        vehicle = Vehicle.objects.create(
            make = "Mercedes-Benz",
            model = "CLS300",
            fuel = 'Dyzelinas',
            advertisement = advertisement,
            year = dateparser.parse('2000-02-01'),
            seller = self.seller)
        criteria = SearchCriteria.objects.create(make='Mercedes-Benz',
            model="CLS klasė",
            subscriber= self.subscriber)
        self.data.append({
            "seller" : self.seller, 
            "advert" : advertisement,
            "vehicle" : vehicle
        })
        filtered_data = criteria.filter_data(self.data)
        self.assertEquals(len(filtered_data), 1)
        self.assertEquals(filtered_data[0]['seller'].phone_number, '123')
        self.assertIsNotNone(filtered_data[0]['advert'].uid, 1002)
        self.assertIsNotNone(filtered_data[0]['vehicle'].model, "CLS300")

    def testBMWSeries(self):
        advertisement = Advertisement.objects.create(
            location = "Mars",
            uid = 1003, 
            seller = self.seller)
        vehicle = Vehicle.objects.create(
            make = "BMW",
            model = "630 Gran Turismo",
            fuel = 'Dyzelinas',
            advertisement = advertisement,
            year = dateparser.parse('2000-02-01'),
            seller = self.seller)
        criteria = SearchCriteria.objects.create(make='BMW',
            model="6 serija",
            subscriber= self.subscriber)
        self.data.append({
            "seller" : self.seller, 
            "advert" : advertisement,
            "vehicle" : vehicle
        })
        filtered_data = criteria.filter_data(self.data)
        self.assertEquals(len(filtered_data), 1)
        self.assertEquals(filtered_data[0]['seller'].phone_number, '123')
        self.assertIsNotNone(filtered_data[0]['advert'].uid, 1003)
        self.assertIsNotNone(filtered_data[0]['vehicle'].model, "630 Gran Turismo")

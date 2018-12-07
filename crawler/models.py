from django.core.mail import EmailMessage
from django.db import models
from django.utils import timezone 
from model_utils import Choices

import datetime, dateparser
from enum import Enum

class Seller(models.Model):
    # Unique indentify seller by his phone number
    phone_number = models.TextField(unique = True, blank=False)    
    Field = Choices(
        ('number', 'NUMBER', 'Number'))
    
    @staticmethod
    def create_from_dict(seller):
        '''
        Creates seller record from dict obj
        params:
            seller: seller data dict
        returns: model record instance
        '''
        return Seller.objects.get_or_create(phone_number=seller[Seller.Field.NUMBER])

    def __str__(self): 
        return self.phone_number

class Advertisement(models.Model):
    # utcnow = datetime.datetime.utcnow()
    utcnow = timezone.now()
    comment = models.TextField(null=True)
    location = models.CharField(max_length=30)
    url = models.TextField()
    uid = models.DecimalField(decimal_places=2, max_digits=20, unique = True)
    price = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    seller = models.ForeignKey(Seller,
        on_delete=models.CASCADE,
        default=None)

    def __str__(self):
        return str(int(self.uid))

class Vehicle(models.Model):
    make = models.CharField(max_length=20, null=False, default=None)
    model = models.CharField(max_length=20, null=False, default=None)
    year = models.DateField(null=True)
    odometr_value = models.CharField(max_length=20, null=True)
    deffects = models.CharField(max_length=50, null=True)
    engine = models.CharField(max_length=30, null=True)
    transmission = models.CharField(max_length=20, null=True)
    fuel = models.CharField(max_length=20, null=True)
    technical_inspection = models.DateField(null=True)
    seller = models.ForeignKey(Seller,
        on_delete=models.CASCADE,
        null=False, 
        default=None)
    advertisement = models.OneToOneField(Advertisement,
        on_delete=models.CASCADE,
        null=False,
        default=None)
    Field = Choices(('make', 'MAKE', 'Manufacturer'),
                    ('model', 'MODEL', 'Model'),
                    ('Pagaminimo data', 'AGE', 'Year of make'),
                    ('Rida', 'RANGE', 'Mileage in km'),
                    ('Defektai', 'ISSUES', 'Issues'), 
                    ('Variklis', 'ENGINE', 'Engine'), 
                    ('Pavarų dėžė', 'GEARBOX', 'Transmission'), 
                    ('Kuro tipas', 'FUEL', 'Fuel type'), 
                    ('Tech. apžiūra iki', 'INSPECT', 'Technical inspection till'))

    @staticmethod
    def merge_params(vhcl):
        '''
        Merge provided vehicle data params with Vehicle model params 
        params:
            vhcl: advert data dict
        returns: Vehicle model instance
        '''
        vehicle = Vehicle()
        vehicle.make = vhcl[Vehicle.Field.MAKE] if Vehicle.Field.MAKE in vhcl else None
        vehicle.model = vhcl[Vehicle. Field.MODEL] if Vehicle.Field.MODEL in vhcl else None
        vehicle.engine = vhcl[Vehicle.Field.ENGINE] if Vehicle.Field.ENGINE in vhcl else None
        vehicle.transmission = vhcl[Vehicle.Field.GEARBOX] if Vehicle.Field.GEARBOX in vhcl else None
        vehicle.fuel = vhcl[Vehicle.Field.FUEL] if Vehicle.Field.FUEL in vhcl else None
        vehicle.deffects = vhcl[Vehicle.Field.ISSUES] if Vehicle.Field.ISSUES in vhcl else None
        vehicle.odometr_value = vhcl[Vehicle.Field.RANGE] if Vehicle.Field.RANGE in vhcl else None
        vehicle.year = dateparser.parse(vhcl[Vehicle.Field.AGE]) if Vehicle.Field.AGE else None
        vehicle.technical_inspection = dateparser.parse(vhcl[Vehicle.Field.INSPECT]) if Vehicle.Field.INSPECT in vhcl else None
        return vehicle

    def __str__(self):
        return '{} {} {}'.format(self.make, self.model, self.year.year)

class Subscriber(models.Model):

    ROLES = Choices(('administrator', 'ADMIN', 'Administrator'), 
                    ('user', 'USER', 'User')) 
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    # Subscribe to email notifications
    subscribed = models.BooleanField(default=True)
    role = models.CharField(max_length=30, choices=ROLES, default=ROLES.USER)

    def notify(self, message):
        '''
        Notifies particular subscriber
        '''
        # TODO
        pass
    
    def notify_instant_adverts(self, data):
        '''
            Advert data - vehicle,
            Tikrinimo seka : town, make, model, year_from, year_to
        '''
        
        search_criterias = SearchCriteria.objects.filter(subscriber_pk=self.id)
        # records = search_criterias.foo.filter_data(data)
        email = EmailMessage('SKELBIMAI', message, to=Subscriber.get_subscribed_emails())
        pass

    @staticmethod
    def notify_all(message):
        '''
        Notifies all subscibed Subscibers
        '''
        email = EmailMessage('SKELBIMAI', message, to=Subscriber.get_subscribed_emails())
        email.send()

    @staticmethod
    def get_subscribed_emails():
        '''
        Returns subscibed Subscirers emails
        '''
        subscr_list = []
        subscr_qs = Subscriber.objects.filter(subscribed=True)
        for subscr in subscr_qs.values():
            subscr_list.append(subscr['email'])
        return subscr_list

    def __str__(self):
        return '{} {}'.format(self.name, self.surname)

class SearchCriteria(models.Model):

    CITIES = Choices(('Vilnius', 'Vilnius'), ('Kaunas', 'Kaunas'))
    make = models.CharField(max_length=100, null=True)
    model = models.CharField(max_length=100, null=True)
    year_from = models.DateField(null=True)
    year_to = models.DateField(null=True)
    city = models.CharField(max_length=100, null=True, choices=CITIES)
    subscriber = models.ForeignKey(Subscriber,
        on_delete=models.CASCADE,
        default=None)
        
    def _filter_cities(self, recs):
        '''
        returns filtered records by advert location

        recs: [{'seller': Seller, 'advert': Advertisement, 'vehicle': Vechicle}]
        returns: array
        '''
        filtered_recs = []
        if (self.city is not None):
            for rec in recs:
                if (self.city is rec['advert'].location):
                    filtered_recs.append(rec)
            # returns records associated with that city
            return filtered_recs
        else:
            # returns all records, because city was not set
            return recs
        
    def _filter_make(self, recs):
        '''
        returns filtered records by vechicle make

        recs: [{'seller': Seller, 'advert': Advertisement, 'vehicle': Vechicle}]
        returns: array
        '''
        filtered_recs = []
        if (self.make is not None):
            for rec in recs:
                if (self.make is rec['vehicle'].make):
                    filtered_recs.append(rec)
                return filtered_recs
        else: 
            return recs
        
    def _filter_model(self, recs):
        '''
            returns filtered records by vechicle model
        ''' 
        filtered_recs = []
        if (self.model is not None):
            for rec in recs:
                if (self.model is rec['vehicle'].model):
                    filtered_recs.append(rec)
                return filtered_recs
        else: 
            return recs
        
    def _filter_year_range(self, recs):
        '''
            returns filtered records by year range

            recs: [{'seller': Seller, 'advert': Advertisement, 'vechicle': Vechicle}]
            returns: array
        '''
        filtered_recs = []
        if (self.year_from is not None and self.year_to is not None):
            for rec in recs:
                if (self.year_from <= rec['vehicle'].year 
                    and self.year_to >= rec['vehicle'].year):
                    filtered_recs.append(rec)
            return filtered_recs
        elif (self.year_from is not None):
            for rec in recs:
                if (self.year_from <= rec['vehicle'].year):
                    filtered_recs.append(rec)
            return filtered_recs
        elif (self.year_to is not None):
            for rec in recs:
                if (self.year_to >= rec['vehicle'].year):
                    filtered_recs.append(rec)
            return filtered_recs
        else:
            return recs

    def filter_data(self, data):
        '''
            Filter advert data by search criterias
            Check sequence: town, make, model, year_range
            
            data: [{'seller': Seller, 'advert': Advertisement, 'vehicle': Vechicle}]
            returns: filtered array

        '''
        recs = self._filter_cities(data)
        recs = self._filter_make(recs)
        recs = self._filter_model(recs)
        recs = self._filter_year_range(recs)
        return recs

    def __str__(self):
        return '{} {}'.format(self.make, self.model)

class CookieStore(models.Model):
    NAMES = Choices(
        ('instant', 'INSTANT', 'Instant'),
        ('weekly', 'WEEKLY', 'Weekly'))
    
    name = models.CharField(max_length=30, choices=NAMES, unique=True)
    value = models.TextField()
    url = models.TextField()

class WebDriverSession(models.Model):

    browser = models.CharField(max_length=30)
    uid = models.TextField(null=False)
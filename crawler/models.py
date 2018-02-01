from django.db import models
from django.utils import timezone 
from model_utils import Choices

import datetime
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

class Advertisement(models.Model):
    # utcnow = datetime.datetime.utcnow()
    utcnow = timezone.now()
    comment = models.TextField(null=True)
    location = models.CharField(max_length=20)
    url = models.TextField()
    uid = models.DecimalField(decimal_places=2, max_digits=10, unique = True)
    price = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(default=utcnow)
    deleted_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    seller = models.ForeignKey(Seller,
        on_delete=models.CASCADE,
        default=None)

class Vehicle(models.Model):
    make = models.CharField(max_length=20, null=False, default=None)
    model = models.CharField(max_length=20, null=False, default=None)
    year = models.DateField(null=True)
    odometr_value = models.CharField(max_length=20, null=True)
    deffects = models.CharField(max_length=20)
    engine = models.CharField(max_length=30)
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
            advert: advert data dict
        returns: model instance
        '''
        vehicle = Vehicle()
        vehicle.make = vhcl[Vehicle.Field.MAKE]
        vehicle.model = vhcl[Vehicle. Field.MODEL]
        vehicle.odometr_value = vhcl[Vehicle.Field.RANGE]
        vehicle.deffects = vhcl[Vehicle.Field.ISSUES]
        vehicle.engine = vhcl[Vehicle.Field.ENGINE]
        vehicle.transmission = vhcl[Vehicle.Field.GEARBOX]
        vehicle.fuel = vhcl[Vehicle.Field.FUEL]
        vehicle.year = datetime.datetime.strptime(vhcl[Vehicle.Field.AGE], '%Y-%m').date()
        vehicle.technical_inspection = datetime.datetime.strptime(
            vhcl[Vehicle.Field.INSPECT], '%Y-%m').date()
        return vehicle
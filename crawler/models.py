from django.db import models
from django.utils import timezone 

import datetime

class Seller(models.Model):
    # Unique indentify seller by his phone number
    phone_number = models.TextField(unique = True, blank=False)

class Advertisement(models.Model):
    # utcnow = datetime.datetime.utcnow()
    utcnow = timezone.now()
    comment = models.TextField(null=True)
    location = models.CharField(max_length=20)
    url = models.TextField()
    uid = models.DecimalField(decimal_places=2, max_digits=10, blank=False)
    price = models.CharField(max_length=7, blank=True)
    created_at = models.DateTimeField(default=utcnow)
    deleted_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    seller = models.ForeignKey(Seller,
        on_delete=models.CASCADE,
        default=None)

class Vehicle(models.Model):
    manufacturer = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    year = models.DateField()
    odometr_value = models.DecimalField(decimal_places=2, max_digits=7)
    deffects = models.BooleanField()
    engine = models.CharField(max_length=30)
    transmission = models.CharField(max_length=20)
    fuel = models.CharField(max_length=20)
    technical_inspection = models.DateField()
    seller = models.ForeignKey(Seller,
        on_delete=models.CASCADE,
        null=False,
        blank=False, 
        default=None)
    advertisement = models.OneToOneField(Advertisement,
        on_delete=models.CASCADE,
        null=False,
        blank=False, 
        default=None)


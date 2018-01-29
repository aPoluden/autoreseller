from django.db import models

class Seller(models.Model):
    # Unique indentify seller by his phone number
    phone_number = models.TextField(unique = True)

class Advertisement(models.Model):
    comment = models.TextField()
    location = models.CharField(max_length=20)
    url = models.TextField()
    uid = models.DecimalField(decimal_places=2, max_digits=10)
    price = models.CharField(max_length=7)
    created_at = models.DateTimeField()
    deleted_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True)

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
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True)
    advertisement = models.OneToOneField(Advertisement, on_delete=models.SET_NULL, null=True, blank=True)


from django.contrib import admin
from .models import Seller, Advertisement, Vehicle, Subscriber
# Register your models here.
admin.site.register(Seller)
admin.site.register(Advertisement)
admin.site.register(Vehicle)
admin.site.register(Subscriber)
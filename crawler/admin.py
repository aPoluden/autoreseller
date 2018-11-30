from django.contrib import admin
from .models import Seller, Advertisement, Vehicle, Subscriber, SearchCriteria
from .forms import MakeForm

# Register your models here.
admin.site.register(Seller)
admin.site.register(Advertisement)
admin.site.register(Vehicle)
admin.site.register(Subscriber)

class SearchCriteriaAdmin(admin.ModelAdmin):
    form = MakeForm
    model = SearchCriteria

admin.site.register(SearchCriteria, SearchCriteriaAdmin)
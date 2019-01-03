from django.shortcuts import render

from crawler.resources.dataset import makes_models

from dal.autocomplete import Select2ListView

from django.views.generic import ListView
from crawler.models import Advertisement

class CarMakeAutocompleteFromList(Select2ListView):
    
    def get_list(self):
        make = self.forwarded.get('make', None)
        qs = makes_models
        if make:
            return qs[make]

class IndexView(ListView):
    template_name = 'crawler/index.html'
    context_object_name = 'advertisement_list'

    def get_queryset(self):
        '''
            Return the last five advertisements"""
        '''
        return Advertisement.objects.order_by('-created_at')[:5]
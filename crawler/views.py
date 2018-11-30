from django.shortcuts import render

from crawler.resources.dataset import makes_models

from dal.autocomplete import Select2ListView

class CarMakeAutocompleteFromList(Select2ListView):
    
    def get_list(self):
        make = self.forwarded.get('make', None)
        qs = makes_models
        if make:
            return qs[make]
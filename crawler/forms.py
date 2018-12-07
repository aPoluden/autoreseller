from dal import autocomplete

from django import forms

from crawler.resources.dataset import models, makes

MAKES = makes

def get_model_list():
    return models

class MakeForm(forms.ModelForm): 
    make = forms.ChoiceField(choices=MAKES)
    model = autocomplete.Select2ListChoiceField(
        choice_list=get_model_list,
        widget=autocomplete.ListSelect2(url='model-list-autocomplete', forward=['make'])
    )
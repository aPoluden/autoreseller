from model_utils import Choices

makes_models = {
    "Audi": ["A3", "A4"],
    "Skoda": ["Octavia", "Fabia"]
}

makes = (('Audi', 'Audi'), 
         ('Skoda', 'Skoda'))

models = ["A3", "A4", "Octavia", "Fabia"]

cities = Choices(('Vilnius', 'Vilnius'), ('Kaunas', 'Kaunas'))

fuels = (('Benzinas', 'Benzinas'), ('Dyzelinas', 'Dyzelinas'))
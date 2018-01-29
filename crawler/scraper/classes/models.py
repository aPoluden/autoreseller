import datetime

class Advertisement:
    
    # Advertisement attributes 
    id, name, url, comments = None, None, None, None
    
    def __init__(self):
        # UTC timestamp when Advertisement instance was created
        # FIXME: This solution is not accurate
        self.created_at = datetime.datetime.utcnow()

class Car:
    
    # Car attibutes
    number_plate, attributes = None, {}

    def __init__(self): 
        pass

class Seller: 
    
    # Seller attributes
    phone_numbers = []
    
    def __init__(self):
        pass 

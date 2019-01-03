import urllib, requests, json
from bs4 import BeautifulSoup

def get_fuels():
    i = 0
    fuels = []
    response = requests.post('https://autoplius.lt')
    soup = BeautifulSoup(response.content, 'html.parser')
    options = soup.find_all('select', id='fuel_id')[0].find_all('option')
    for option in options:
        i+=1
        value = None
        if (len(options) == i):
            value = option.contents[0].replace('<\\/option>', '').replace('\\', '').replace('\\', '')
            value = value.replace(value[len(value) - 1], '')
        else:
            value = option.contents[0].replace('<\\/option>', '').replace('\\', '').replace('\\', '')
        if (value != '- Pasirinkite -' and value != '-kita-'):
            fuels.append(value)
    return fuels

def get_cities():
    cities = []
    i = 0
    params = {
        'parent_id': 1,
        'target_id': 'fk_place_cities_id',
        'project': 'autoplius',
        'category_id': 2, 
        'type': 'search', 
        'my_anns' : 'false', 
        '__block': 'ann_ajax_0_plius', 
        '__opcode': 'ajaxGetChildsTo'
    }
    response = requests.post('https://autoplius.lt/paieska/naudoti-automobiliai', data=params)
    soup = BeautifulSoup(response.content, 'html.parser')
    options = soup.find_all('option')
    for option in options:
        i+=1
        value = None
        if (len(options) == i):
            value = option.contents[0].replace('<\\/option>', '').replace('\\', '').replace('\\', '')
            value = value.replace(value[len(value) - 1], '')
        else:
            value = option.contents[0].replace('<\\/option>', '').replace('\\', '').replace('\\', '')
        if (value != '- Pasirinkite -' and value != '-kita-'):
            cities.append(value)
    return cities

def get_makes():
    makes = []
    response = requests.get('https://autoplius.lt')
    soup = BeautifulSoup(response.content, 'html.parser')
    options = soup.find_all('select', id='make_id')[0].find_all('option')
    for option in options:
            makes.append({'name': option.text, 'id': option.attrs['value']})
    return makes

def get_models(make_id):
    models = []
    params = {
        'parent_id': make_id,
        'target_id': 'model_id',
        'project': 'autoplius',
        'category_id': 2, 
        'type': 'search', 
        'my_anns' : 'false', 
        '__block': 'ann_ajax_0_plius', 
        '__opcode': 'ajaxGetChildsTo'
    }
    i = 0
    r = requests.post("https://autoplius.lt", data=params)
    soup = BeautifulSoup(r.content, 'html.parser')
    options = soup.find_all('option')
    for option in options:
        i+=1
        value = None
        if (len(options) == i):
            value = option.contents[0].replace('<\\/option>', '').replace('\\', '').replace('\\', '')
            value = value.replace(value[len(value) - 1], '')
        else:
            value = option.contents[0].replace('<\\/option>', '').replace('\\', '').replace('\\', '')
        if (value != '- Pasirinkite -' and value != '-kita-'):
            models.append(value)
    return models

def make_post(): 
    params = {'make_id': 104, 'model_id': 1409, 'make_date': '2006' }
    r = requests.post("https://autoplius.lt", data=params)

if __name__ == "__main__":
    make_models = {}
    models = []
    makes = ()
    cities = ()
    fuels = ()
    fuels_tmp = get_fuels()
    makes_tmp = get_makes()
    cities_tmp = get_cities()
    for make in makes_tmp:
        models_tmp = get_models(make['id'])
        make_models[make['name']] = models_tmp
        models.extend(models_tmp)
        tmp = (make['name'], make['name'])
        makes = makes + (tmp,)
    for city in cities_tmp:
        tmp = (city, city)
        cities = cities + (tmp,)
    for fuel in fuels_tmp:
        tmp = (fuel, fuel)
        fuels = fuels + (tmp,)
    # write makes_models json
    with open('makes_models.json', 'w') as fp:
        json.dump(make_models, fp)
    # write models json
    with open('models.json', 'w') as fp:
        json.dump(models, fp)
    # write makes to file
    with open('makes.txt', 'w') as fp:
        core = '\n'.join('("{}", "{}"),'.format(x[0],x[1]) for x in makes)
        fp.write('(' + core + ')')
    # write cities to file
    with open('cities.txt', 'w') as fp:
        core = '\n'.join('("{}", "{}"),'.format(x[0],x[1]) for x in cities)
        fp.write('(' + core + ')')
    # write fuels to file
    with open('fuels.txt', 'w') as fp:
        core = '\n'.join('("{}", "{}"),'.format(x[0],x[1]) for x in fuels)
        fp.write('(' + core + ')')
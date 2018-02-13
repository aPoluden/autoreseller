from bs4 import BeautifulSoup
import urllib, requests, logging
from requests.exceptions import ConnectionError, TooManyRedirects, Timeout, RequestException

from crawler.scraper.classes.options import AdvertOptions, Bot
from crawler.scraper.classes.models import Advertisement
from crawler.scraper.classes.robot import DefaultRobot, YandexRobot
from crawler.scraper.utils import tor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# handler = logging.RotatingFileHandler('hello.log')
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)

class PortalScraper:

    def __init__(self, advert_type, ):
        self.advert_type = advert_type

    def scrape_particular_advert(self, url, path=None):
        pass

    def scrape_entire_adverts(self):
        pass

class AutoPScraper(PortalScraper):

    def __init__(self, advert_type, robot_type = None):
        super(AutoPScraper, self).__init__(advert_type)
        if advert_type == AdvertOptions.CARS:
            self.scraper = AutoPCarScraper(robot_type)
    
    def scrape_particular_advert(self, url, path=None):
        return self.scraper.get_particular_vehicle(url, path)

    def scrape_entire_adverts(self):
        return self.scraper.get_entire_vehicles()

    def type(self):
        '''
        returns: scraper instance
        '''
        return self.scraper

    def bot(self):
        '''
        returns: scraper bot
        '''
        return self.scraper.bot()

class VehicleScraper:

    def __init__(self, robot_type=None):
        self.robot = (YandexRobot() if robot_type is Bot.YANDEX else DefaultRobot())

    def bot(self): 
        return self.robot

    def get_particular_vehicle(self, url, path=None):
        pass
    
    def get_entire_vehicles(self): 
        pass

class AutoPCarScraper(VehicleScraper):
    
    def __init__(self, robot_type=None):
        super(AutoPCarScraper, self).__init__(robot_type)

    def remove_spaces(self, raw): 
        return raw.replace(' ', '').replace('\n', '')

    def get_car_advert_data(self, url, path=None):
        '''
        Scrapes AutoP store car advertisement
        returns: advertisement data
        '''
        advert, seller, vehicle = {}, {}, {}
        # content = self.page_content(url, path)
        content = self.robot.visit_url(url)
        if content is None:
            logger.warn('Advert %s not reachable', url)
            return None
        soup = BeautifulSoup(content, 'html.parser')
        element = soup.find_all(class_='add-to-bookmark')[0]
        advert_info = soup.find_all(class_='classifieds-info')[0]
        vehicle_specs = advert_info.find_all(class_='announcement-parameters')
        advert['uid'] = element.attrs['data-id']
        advert['location'] = self.remove_spaces(soup.find(class_='owner-location').text)
        seller['number'] = self.remove_spaces(soup.find(class_="announcement-owner-contacts").a.text)
        for param in vehicle_specs:
            # Vehicle specials
            param_rows = param.find_all('tr')
            for row in param_rows:
                spec_name = row.th.text
                spec_value = row.td.text
                # Price in Lithiania
                if spec_name == 'Kaina Lietuvoje':
                    # Special price occasion
                    advert['price'] = spec_value.split('€')[0] + '€'
                vehicle[spec_name] = spec_value
            # Split vehicle name to Model and Make
            make_model = advert_info.h1.text.split(',')[0]
            vehicle['make'] = make_model.split(' ')[0]
            vehicle['model'] = make_model.split(' ')[1]
        try:
            # Advert attributes that could be not defined
            advert['comment'] = advert_info.find(class_='announcement-description').text
        except AttributeError as e:
            pass
        return {'vehicle': vehicle, 'advert': advert, 'seller': seller}
        
    def get_all_car_adverts_data(self):
        '''
        Scrapes all STORE car advertisements
        returns: all STORE car advertisements
        '''
        soup = None
        current_page = 1
        url='https://autoplius.lt/skelbimai/naudoti-automobiliai'
        list_page = '/skelbimai/naudoti-automobiliai?page_nr={}'
        while True:
            list_url = url + list_page.format(current_page)
            #content = self.page_content(list_url)
            content = self.robot.visit_url(list_url)
            if content is None:
                logger.warn('Advert list %s not reachable')
                yield None
            soup = BeautifulSoup(content, 'html.parser')
            adverts_list = soup.find_all(class_='announcement-item')
            for advert in adverts_list:
                advert_url = advert['href']
                advert_data = self.get_car_advert_data(advert_url)
                logger.debug(advert_data)
                yield advert_data
            current_page += 1
    
    def get_particular_vehicle(self, url, path=None):
        return self.get_car_advert_data(url, path)

    def get_entire_vehicles(self):
        return self.get_all_car_adverts_data()

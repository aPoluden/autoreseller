from bs4 import BeautifulSoup
import urllib, requests, logging
from requests.exceptions import ConnectionError, TooManyRedirects, Timeout, RequestException

from crawler.scraper.classes.options import AdvertOptions, Bot
from crawler.scraper.classes.models import Advertisement
from crawler.scraper.classes.robot import DefaultRobot
from crawler.scraper.utils import tor

logger = logging.getLogger(__name__)

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
        self.robot = DefaultRobot()

    def bot(self): 
        return self.robot

    def get_particular_vehicle(self, url, path=None):
        pass
    
    def get_entire_vehicles(self): 
        pass

class AutoPCarScraper(VehicleScraper):
    
    def __init__(self, robot_type=None):
        super(AutoPCarScraper, self).__init__(robot_type)

    def _remove_spaces(self, raw):
        return raw.replace(' ', '').replace('\n', '')

    def _resolve_make_model(self, data):
        # 0 make and model 
        makemodel = data.replace('\n', '').split(',')[0].split(' ')
        make, model = makemodel[0], makemodel[1]
        return (make, model)

    def get_car_advert_data(self, url, path=None):
        '''
        Scrapes AutoP store car advertisement
        returns: advertisement data
        '''
        advert, seller, vehicle = {}, {}, {}
        supported_params = ['Pagaminimo data', 
                            'Rida',
                            'Defektai', 
                            'Variklis',
                            'Pavarų dėžė',
                            'Kuro tipas',
                            'Tech. apžiūra iki']
        # content = self.page_content(url, path)
        content = self.robot.visit_url(url)
        if content is None:
            logger.warn('Advert %s not reachable', url)
            return None
        advert['url'] = url
        soup = BeautifulSoup(content, 'html.parser')
        # resolve make and model
        vehicle['make'], vehicle['model'] = self._resolve_make_model(soup.find_all(class_='page-title')[0].text)        # resolve advert id
        bookmark_div = soup.find_all(class_='add-to-bookmark')[0]
        advert['uid'] = bookmark_div.attrs['data-id']
        # resolve advert price
        price_div = soup.find_all(class_='price')[0]
        advert['price'] = price_div.text.replace(' ', '').replace('\n', '')
        advert['location'] = soup.find(class_='owner-location').text.strip()
        seller['number'] = self._remove_spaces(soup.find(class_="owner-phone").text)
        # from 2 index starts valueable advert data
        advert_data = soup.find_all(class_='parameter-row')[2:]
        for data in advert_data:
            label = data.find(class_='parameter-label').text.strip()
            if label in supported_params:
                value = data.find(class_='parameter-value').text.strip()
                vehicle[label] = value
        try:
            # Advert attributes that could be not defined
            advert['comment'] = soup.find_all(class_='announcement-description').text
        except AttributeError as e:
            pass
        return {'vehicle': vehicle, 'advert': advert, 'seller': seller}
        
    def get_all_car_adverts_data(self, page=1):
        '''
        Scrapes all STORE car advertisements
        returns: all STORE car advertisements
        '''
        soup = None
        current_page = page
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
            logger.info('Scraped {} page'.format(current_page))
            current_page += 1
    
    def get_instant_car_advert_data(self):
        '''
        Scrapes only new car adverisements
        returns: scraped car advert data
        '''
        #https://autoplius.lt/mano-paieskos?slist=430359403&category_id=2&older_not=-1
        #https://autoplius.lt/mano-paieskos?slist=430359403&category_id=2&older_not=-1&page_nr=2
        instant_url = self.robot.fake_instant_advert_session()
        current_page = 1
        # Visit top url before scraping
        self.robot.visit_url(self.robot.top_url)
        while True:
            content = self.robot.visit_url(instant_url)
            soup = BeautifulSoup(content, 'html.parser')
            logger.debug(soup)
            new_adverts = soup.find_all(class_='auto-lists lt cl')
            if len(new_adverts) > 0: 
                new_cars_html = new_adverts[0].find_all(class_='announcement-item')
                for new_car_html in new_cars_html:
                    yield self.get_car_advert_data(new_car_html['href'])
                if len(new_cars_html) is 20:
                    # More than one advert page to scrape
                    current_page += 1
                    instant_url = instant_url + '&page_nr={}'.format(current_page)
                else:
                    current_page += 1
                    instant_url = instant_url + '&page_nr={}'.format(1)
                    yield None
            else:
                yield None

    def get_particular_vehicle(self, url, path=None):
        return self.get_car_advert_data(url, path)

    def get_entire_vehicles(self):
        return self.get_all_car_adverts_data()

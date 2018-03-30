import urllib, requests, logging, time, ast
from selenium import webdriver
from requests.exceptions import RequestException

from crawler.models import CookieStore

# Robot description - send requests. Fake user agent. Fake session. Handle RequestExceptions

logger = logging.getLogger(__name__)

class DefaultRobot():

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'
    top_url = 'https://autoplius.lt'
    instant_cars_advert_search_url = 'https://autoplius.lt/skelbimai/naudoti-automobiliai?older_not=-1'

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({ 'User-Agent': self.user_agent })

    def visit_url(self, url):
        try: 
            self.resp = self.session.get(url)
            # Check if not blacklisted
            if self.resp.status_code == 429:
                logger.warn('IP blacklisted')
                return None
        except RequestException as e:
            logger.warn(e)
            return None
        return self.resp.content

    def fake_browsing(self, url_type):
        '''
        Fakes browsing over website
        returns: browser instance 
        '''
        browser = webdriver.Firefox()
        browser.get(self.top_url)
        browser.get(url_type)
        time.sleep(2) # TODO remove ?
        browser.get(self.top_url)
        # find search preference element
        item = browser.find_element_by_class_name('search-item')
        item.click()
        return browser

    def fake_instant_advert_session(self):
        '''
        Initilizes session using browser session
        '''
        instant_advert_url = ''
        if CookieStore.objects.filter(name=CookieStore.NAMES.INSTANT).exists():
            # Get instant advert fake cookie session
            cs = CookieStore.objects.filter(name=CookieStore.NAMES.INSTANT).first()
            # Convert str to list
            cookies = ast.literal_eval(cs.value)
            self.session.cookies.update({c['name']:c['value'] for c in cookies})
            instant_advert_url = cs.url
            # TODO something with cookie
        else:
            # Init instant fake cookie session
            cs = CookieStore(name=CookieStore.NAMES.INSTANT)
            browser = self.fake_browsing(self.instant_cars_advert_search_url)
            self.session.cookies.update({c['name']:c['value'] for c in browser.get_cookies()})
            # Convert cookie list to str
            cs.value = str(browser.get_cookies())
            cs.url = browser.current_url
            cs.save()
            instant_advert_url = browser.current_url
            browser.close()
        return instant_advert_url

    def fake_week_advert_session():
        # TODO implement in future 
        pass
    
    def say_hello(self):
        return "Hello, I'm Default robot"

    def get_user_agent(self): 
        return self.user_agent

class YandexRobot(DefaultRobot):

    sessionID = ''
    user_agent = 'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)'
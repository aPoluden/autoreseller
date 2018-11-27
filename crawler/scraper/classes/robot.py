import urllib, requests, logging, time, ast
from selenium import webdriver
from requests.exceptions import RequestException

from autoreseller import settings

from crawler.models import CookieStore, WebDriverSession
from crawler.scraper.classes.options import Portals

# Robot description - send requests. Fake user agent. Fake session. Handle RequestExceptions

logger = logging.getLogger(__name__)

class DefaultRobot():
    '''
        Robot searches only autoplius car instant advertisements
    '''
    _executor_url = 'http://autoreseller_geckodriver_1:4444'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'
    top_url = 'https://autoplius.lt'
    instant_cars_advert_init_url = 'https://autoplius.lt/skelbimai/naudoti-automobiliai?older_not=-1'
    instant_cars_advert_check_url = None
    page_counter = 1 
    browser = None

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({ 'User-Agent': self.user_agent })

    def visit_url(self, url):
        '''
            Depricated
            Failed to establish a new connection: [Errno -3]
            Temporary failure in name resolution
        '''
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

    def visit_next_instant_cars_page(self):
        '''
        Visit next instant car advert list page
        return page content
        '''
        temp_url = ''
        if (self.instant_cars_advert_check_url is not None):
            # copy string with page_nr={} for later uses
            temp_url = self.instant_cars_advert_check_url
            self.page_counter += 1
            self.self.instant_cars_advert_check_url = self.instant_cars_advert_check_url.format(self.page_counter)
            self.browser.get(self.instant_cars_advert_check_url)
            logger.info('next cars page: {}'.format(self.page_counter))
            return self.browser.page_source
        self.instant_cars_advert_check_url = temp_url
        self.page_counter = 1
        return None

    def visit_url_through_browser(self, url):
        '''
        Visit url through browser
        returns html source
        '''
        if (self.browser is not None): 
            self.browser.get(url)
            logger.debug('visit url: {}'.format(url))
            return self.browser.page_source

    def _instant_cars_advert_search_init(self):
        '''
        Fake instant advert search
        '''
        logger.info('init instant search')
        self.browser.get(self.top_url)
        self.browser.get(self.instant_cars_advert_init_url)
        self.browser.get(self.top_url)
    
    def _visit_instant_car_advert_list(self):
        '''
            Enter INITILIZED instant car advert list
        '''
        logger.info('visit instant search')
        self.browser.get(self.top_url)
        # search-info has-new
        search_item = self.browser.find_element_by_class_name('search-item')
        search_item.click()
        return self.browser

    def _reatach_to_existing_driver_session(self, session_id, executor_url):
        '''
        Hack: how to reatach to existing Firefox session
        source: http://tarunlalwani.com/post/reusing-existing-browser-session-selenium/
        '''
        logger.info('reataching to existing webdriver session')
        from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
        # Save the original function, so we can revert our patch
        org_command_execute = RemoteWebDriver.execute

        def new_command_execute(self, command, params=None):
            if command == "newSession":
                # Mock the response
                return {'success': 0, 'value': None, 'sessionId': session_id}
            else:
                return org_command_execute(self, command, params)
        # Patch the function before creating the driver object
        RemoteWebDriver.execute = new_command_execute
        new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        new_driver.session_id = session_id
        # Replace the patched function with original function
        RemoteWebDriver.execute = org_command_execute
        logger.info('webdriver session id: {}'.format(session_id))
        return new_driver

    def _init_browser_session(self):
        '''
        Initialize webdriver session with browser or reuse existing
        '''
        if (WebDriverSession.objects.all().count() > 0):
            logger.info('acquire webdriver session')
            # acquire session from db
            session = WebDriverSession.objects.all()[0]
            self.browser = self._reatach_to_existing_driver_session(session.uid, self._executor_url)
        else:
            # saving session for later use
            logger.info('create new webdriver session')
            self.browser = webdriver.Remote(
                command_executor = self._executor_url,
                desired_capabilities={})
            WebDriverSession.objects.create(
                uid = self.browser.session_id,
                browser = webdriver.DesiredCapabilities.FIREFOX['browserName'])
            # Initialize instant advert search url
            self._instant_cars_advert_search_init()

    def get_instant_adverts_page_content(self):
        '''
            Fetches instant car advert page list content
            retuns: html page content
        '''
        logger.info("")
        if (self.browser is None):
            self._init_browser_session()
        self._visit_instant_car_advert_list()
        # Get page content
        self.instant_cars_advert_check_url = self.browser.current_url + '&page_nr={}'
        return self.browser.page_source

    def close_session(self):
        '''
            Close webbrowser and delete session ID from DB
        '''
        self.browser.quit()
        session = WebDriverSession.objects.all()[0]
        session.delete()
        self.browser = None
        logging.info('browser session closed')
import urllib, requests, logging

from requests.exceptions import RequestException
# Robot description - send requests. Fake user agent. Fake session. Handle RequestExceptions

logger = logging.getLogger(__name__)

class DefaultRobot():

    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'

    def __init__(self): 
        self.headers = requests.utils.default_headers()
        self.headers.update({
            'User-Agent': self.user_agent,
    })

    def visit_url(self, url):
        try: 
            self.resp = requests.get(url)
            # Check if not blacklisted
            if self.resp.status_code == 429:
                logger.warn('IP blacklisted')
                return None
        except RequestException as e:
            logger.warn(e)
            return None
        return self.resp.content

    def say_hello(self):
        return "Hello, I'm Default robot"

    def get_user_agent(self): 
        return self.user_agent

class YandexRobot(DefaultRobot):

    session = ''
    user_agent = 'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)'

# Old request logic
# def page_content(self, page_url, page_path=None):
#     '''
#     Returns WEB page HTML content
#     params:
#         page_url - web page resource url
#         page_path - web page resource path
#     returns:
#         HTML content
#     '''
#     content = None
#     resp = None

#     user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
#     # https://yandex.com/support/webmaster/robot-workings/check-yandex-robots.html
#     yandex_indexing_bot_agent = 'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)'

#     if self.ip_blocked:
#         # Change ip if it was blocked
#         tor.change_ip()
#         self.ip_blocked = False
#     try:
#         if page_path:
#             content = urllib.request.urlopen(page_path).read()
#         else:
#             headers = requests.utils.default_headers()
#             headers.update({
#                 'User-Agent': yandex_indexing_bot_agent,
#             })
#             resp = self.request(page_url)
#             # Check if not blacklisted
#             if resp.status_code == 429:
#                 self.ip_blocked = True
#                 self.request = tor.request
#                 self.page_content(page_url)
#                 logger.warn('IP blacklisted')
#             content = resp.content
#     except requests.exceptions.Timeout:
#         logger.error('Timeout')
#     except TooManyRedirects:
#         logger.error('Too many redirects')
#     except RequestException:
#         logger.error('Request Exception')
#     except ConnectionError:
#         logger.error('Connection Error')
#     except urllib.error.URLError:
#         logger.error('URL Error')
#     return content
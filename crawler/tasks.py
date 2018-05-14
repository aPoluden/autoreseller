import logging, time, requests
from  django.core.mail import EmailMessage

from autoreseller import celery_app

from crawler.scraper.scraper import Scraper
from crawler.scraper.classes.options import AdvertOptions
from crawler.models import Vehicle, Advertisement, Seller
from crawler.scraper.classes.autopscrapers import AutoPCarScraper 

from celery.contrib import rdb
logger = logging.getLogger(__name__)

crawl_delay = 2

@celery_app.task(name='autoplius-entire-car-advert-crawl')
def daily_advert_check_task(from_page=1):
    '''
    Daily advert crawling. Also Create and Update
    '''
    logger.info('Entire advert check task stared')
    has_adverts = True
    # Vremenno zakomentiroval
    scraper = Scraper()
    scraper.set_autop(AdvertOptions.CARS)
    adverts = scraper.scrape_entire_adverts()
    while has_adverts:
        try:
            advert_data = next(adverts)
            if advert_data:
                advert_uid = advert_data['advert']['uid']
                if not Advertisement.objects.filter(uid = advert_uid).exists():
                    # Advertisement doest't exist: Create new
                    seller = Seller.create_from_dict(advert_data['seller'])[0]
                    advert = Advertisement(**advert_data['advert'])
                    vehicle = Vehicle.merge_params(advert_data['vehicle'])
                    advert.seller = seller
                    advert.save()
                    vehicle.advertisement = advert
                    vehicle.seller = seller
                    vehicle.save()
                    logger.info('Advert {} created'.format(advert_uid))
                else: 
                    # Advertisement exists
                    # TODO track advert changes
                    logger.info('Advert {} updated'.format(advert_uid))
                # Time delay between Advertising scraping
                time.sleep(crawl_delay)
            else:
                # advertisements left to scrape
                logger.info('Entire advert check task finished')
                has_adverts = False
        except Exception as e:
            logger.warn('Advert {} processing fail'.format(advert_data['advert']['url']))
            logger.error(e)
            has_adverts = False

@celery_app.task(name='autoplius-instant-car-notifier')
def instant_advert_notification_task():
    '''
    Checks for new adverts. Creates new adverts in db.
    Notifies by email about new advert.
    '''
    import ipdb; ipdb.set_trace()
    logger.info('Instant advert check task stared')
    has_adverts = True
    instant_advert_urls = 'Hello, this is instant autoplius adverts for the moment:\n'
    scraper = AutoPCarScraper()
    adverts = scraper.get_instant_car_advert_data()
    instant_advert_count = 0
    while has_adverts:
        try:
            advert_data = next(adverts)
            if advert_data:
                advert_uid = advert_data['advert']['uid']
                if not Advertisement.objects.filter(uid = advert_uid).exists():
                    # Advertisement doesn't exist: Create new
                    seller = Seller.create_from_dict(advert_data['seller'])[0]
                    advert = Advertisement(**advert_data['advert'])
                    vehicle = Vehicle.merge_params(advert_data['vehicle'])
                    advert.seller = seller
                    advert.save()
                    vehicle.advertisement = advert
                    vehicle.seller = seller
                    vehicle.save()
                    logger.info('Advert {} created'.format(advert_uid))
                    instant_advert_urls = instant_advert_urls  + advert_data['advert']['url'] + '\n'
                    instant_advert_count += 1
                else: 
                    # Advertisement exists
                    # TODO track advert changes
                    logger.info('Advert {} updated'.format(advert_uid))
                # Time delay between Advertising scraping
                time.sleep(crawl_delay)
            else:
                # advertisements left to scrape
                logger.info('Instant advert check task finished')
                if instant_advert_count > 0:
                    email = EmailMessage('SKELBIMAI', instant_advert_urls, to=[])
                    email.send()
                has_adverts = False
        except Exception as e:
            logger.warn('Advert {} processing fail'.format(advert_data['advert']['url']))
            logger.error(e)
            has_adverts = False

def call_task_repeat(): 
    while True: 
        instant_advert_notification_task()
        time.sleep(420)

@celery_app.task(name='debug')
def periodic_task():
    logger.info("I'm a task")
import logging

from crawler.scraper.scraper import Scraper
from crawler.scraper.classes.options import AdvertOptions
from crawler.models import Vehicle, Advertisement, Seller

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger(__name__)

def daily_advert_check_task():
    '''
    Daily advert crawling. Also Create and Update
    '''
    logger.info('Entire advert check task stared')
    scraper = Scraper()
    scraper.set_autop(AdvertOptions.CARS)
    adverts = scraper.scrape_entire_adverts()
    advert_data = next(adverts) # json
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
            logger.info('Advert {} updated'.format(advert_uid))
    else:
        # advertisements left to scrape
        logger.info('Entire advert check task finished')
        return

def instant_advert_notification_task():
    '''
    Checks for new adverts. Creates new adverts in db.
    Notifies by email about new advert.
    '''
    pass
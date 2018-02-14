import logging, time

from crawler.scraper.scraper import Scraper
from crawler.scraper.classes.options import AdvertOptions
from crawler.models import Vehicle, Advertisement, Seller

logger = logging.getLogger(__name__)

crawl_delay = 2

def daily_advert_check_task():
    '''
    Daily advert crawling. Also Create and Update
    '''
    logger.info('Entire advert check task stared')
    has_adverts = True
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

def instant_advert_notification_task():
    '''
    Checks for new adverts. Creates new adverts in db.
    Notifies by email about new advert.
    '''
    # TODO
    pass
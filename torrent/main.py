import logging
import os
from datetime import datetime
#from dotenv import load_dotenv
import time


from util.torrent_utils import write_shop_index
#load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
os.environ['TZ'] = 'America/Campo_Grande'

# scheduler = BlockingScheduler()


# @scheduler.scheduled_job(trigger='interval', id='create_shop_index', minutes=10)
# def create_shop_index():
#     logger.info(f'Indexing task running at {datetime.now()}')
#     write_shop_index()


if __name__ == '__main__':
    logger.info('Starting index generation')
    while (True):
        write_shop_index()
        time.sleep(120)
    #scheduler.start()

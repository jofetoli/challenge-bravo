#cron/cron.py

from datetime import timedelta
from timeloop import Timeloop
import logging
import sys

logger = logging.getLogger('cron')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

tl = Timeloop()

@tl.job(interval=timedelta(seconds=3))
async def updating_currencies():
    logger.info("starting...")
    client = app['currency_client']
    currencies_dict = client.get_currencies()
    async with app['db'].acquire() as conn:
        registered_currencies_dict = app['db'].get_all_currency(conn)
        for reg_currency in registered_currencies_dict:
            try:
                value = currencies_dict['data']['rates'][reg_currency['code']]
                logger.info(reg_currency['code'] + " " + value)
            except (KeyError, TypeError, ValueError) as e:
                logger.info(e)
    logger.info("ending...")

tl.start(block=True)
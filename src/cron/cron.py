#cron/cron.py

from datetime import timedelta
from aiohttp import web, ClientSession
from integrations.currency_fetcher import CurrencyFetcher
from infrastructure.db import close_pg, init_pg
import infrastructure.db as db
from infrastructure.settings import config
import logging
import sys

import asyncio

cron = {}

logger = logging.getLogger('cron')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
init_pg
logger.setLevel(logging.INFO)

cron['config'] = config

async def updating_currencies(client):
    try:
        logger.info("starting...")
        currencies_dict = await client.get_currencies()
        logger.info("got currencies")
        async with cron['db'].acquire() as conn:
            registered_currencies_dict = await asyncio.wait_for(db.get_all_currency(conn), timeout=3.0) 
            logger.info("got registered currencies")
            for reg_currency in registered_currencies_dict:
                reg_currency['value'] = currencies_dict['data']['rates'][reg_currency['code']]
                currency = await db.update_currency(conn, reg_currency)
                logger.info(reg_currency)
        logger.info("ending...")
    except:
        logger.exception("Something went wrong while updating the currency rates:")

async def main():
    client = CurrencyFetcher(ClientSession())
    await init_pg(cron)
    while True:
        await updating_currencies(client)
        await asyncio.sleep(cron['config']['cron']['update_frequency'])
    await close_pg(cron)

asyncio.run(main())



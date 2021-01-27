#cron/cron.py

from datetime import timedelta
from aiohttp import web, ClientSession
from integrations.currency_fetcher import CurrencyFetcher
from infrastructure.db import close_pg, init_pg
from infrastructure.cache import init_redis
import infrastructure.db as db
from infrastructure.settings import config
from infrastructure.logger import get_logger

import asyncio

cron = {}

cron['logger'] = get_logger('cron')
cron['config'] = config

async def updating_currencies(client):
    try:
        cron['logger'].info("starting...")
        currencies_dict = await client.get_currencies()
        cron['logger'].info("got currencies")
        async with cron['db'].acquire() as conn:
            registered_currencies_dict = await asyncio.wait_for(db.get_all_currency(conn), timeout=3.0) 
            cron['logger'].info("got registered currencies")
            for reg_currency in registered_currencies_dict:
                reg_currency['value'] = currencies_dict['data']['rates'][reg_currency['code']]
                cron['cache'].delete(reg_currency['code'])
                currency = await db.update_currency(conn, reg_currency)
                cron['logger'].info(reg_currency)
        cron['logger'].info("ending...")
    except:
        cron['logger'].exception("Something went wrong while updating the currency rates:")

async def main():
    client = CurrencyFetcher(ClientSession())
    await init_pg(cron)
    init_redis(cron)
    while True:
        await updating_currencies(client)
        await asyncio.sleep(cron['config']['cron']['update_frequency'])
    await close_pg(cron)

asyncio.run(main())



# app/server.py

from aiohttp import web, ClientSession
from api.routes import setup_routes
from settings import config
from integrations.currency_fetcher import CurrencyFetcher
from infrastructure.db import close_pg, init_pg

import logging
import sys

logger = logging.getLogger('bravo')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

app = web.Application()
setup_routes(app)
app['config'] = config
app['currency_client'] = CurrencyFetcher(ClientSession())
app['cache'] = {}
app['logger'] = logger

app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)

web.run_app(app)
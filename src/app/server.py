# src/main.py

from aiohttp import web, ClientSession
from api.routes import setup_routes
from settings import config
from integrations.currency_fetcher import CurrencyFetcher
from infrastructure.db import close_pg, init_pg
from datetime import timedelta
import time
from timeloop import Timeloop
import logging
import sys

logger = logging.getLogger('bravo')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

tl = Timeloop()
@tl.job(interval=timedelta(seconds=3))
def sample_job_every_2s():
    logger.info("rodando...")


app = web.Application()
setup_routes(app)
app['config'] = config
app['currency_client'] = CurrencyFetcher(ClientSession())
app['cache'] = {}
app['logger'] = logger
tl.start(block=False)
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
app.on_cleanup.append(tl.stop)

web.run_app(app)
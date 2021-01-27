# app/server.py

from aiohttp import web, ClientSession
from api.routes import setup_routes
from infrastructure.settings import config
from integrations.currency_fetcher import CurrencyFetcher
from infrastructure.db import close_pg, init_pg
from infrastructure.cache import init_redis
from infrastructure.logger import get_logger


app = web.Application()
setup_routes(app)
app['config'] = config
app['currency_client'] = CurrencyFetcher(ClientSession())
app['logger'] = get_logger('bravo')
init_redis(app)

app.on_startup.append(init_pg)

app.on_cleanup.append(close_pg)

web.run_app(app)
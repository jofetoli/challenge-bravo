# app/server.py

from aiohttp import web, ClientSession

from api.routes import setup_routes
from infrastructure.cache import init_redis
from infrastructure.db import close_pg, init_pg
from infrastructure.logger import get_logger
from infrastructure.settings import config
from integrations.currency_fetcher import CurrencyFetcher


app = web.Application()
setup_routes(app)
app['config'] = config
app['currency_client'] = CurrencyFetcher(ClientSession())
app['logger'] = get_logger('bravo')
app['cache'] = init_redis(app['config'])

app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)

web.run_app(app)
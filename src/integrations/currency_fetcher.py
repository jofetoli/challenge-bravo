#integrations\currency_fetcher.py
from aiohttp import web


class CurrencyFetcher:
    _session = None

    def __init__(self, aiohttp_session):
        self._session = aiohttp_session

    async def get_currencies(self):
        async with self._session.get('https://api.coinbase.com/v2/exchange-rates?currency=USD') as response:
            return await response.json()

    async def get_currency_rate_by_code(self, code):
        currencies = await self.get_currencies()
        try:
            return currencies['data']['rates'][code]
        except (KeyError, TypeError, ValueError) as e:
            raise web.HTTPBadRequest(
                text='You have specified a unknow currency code') from e
        
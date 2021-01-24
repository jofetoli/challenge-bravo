# app/api/controller/currency/views.py
from aiohttp import web
import infrastructure.db as db
from datetime import datetime, timedelta

# GET /
async def index(request):
    async with request.app['db'].acquire() as conn:
        currencies = await db.get_all_currency(conn)
        return web.Response(text=str(currencies))

# PUT /currency/:code
async def add_currency(request):
    async with request.app['db'].acquire() as conn:
        currency = await _get_currency_from_request(conn, request)
        if(currency == None):
            currency_code, currency_rate = await _fetch_currency(request) 
            currency = await db.insert_currency(conn, currency_code, currency_rate)
        elif currency['active'] == 0:
            currency['active'] = 1
            currency = await db.update_currency(conn, currency)
        return web.Response(text=str(currency))

# DELETE /currency/:code
async def rm_currency(request):
    async with request.app['db'].acquire() as conn:
        currency = await _get_currency_from_request(conn, request)
        if(currency == None or currency['active'] == 0):
            raise web.HTTPBadRequest(
                text='You can\'t remove a not registered currency')

        currency['active'] = 0
        currency = await db.update_currency(conn, currency)
        # if currency[code] in request.app['cache']:
        #     request.app['cache'].pop(currency[code])
        return web.Response(text=str(currency))
    
async def _get_currency_code_from_request(request):
    data = await request.post()
    try:
        return str(data['code'])
    except (KeyError, TypeError, ValueError) as e:
        raise web.HTTPBadRequest(
            text='You have not specified a currency code') from e

async def _get_convertion_args_from_request(request):
    data = request.query
    try:
        return str(data['from']), str(data['to']), str(data['amount'])
    except (KeyError, TypeError, ValueError) as e:
        raise web.HTTPBadRequest(
            text='You have not used the api correctly. Ex: "?from=BTC&to=EUR&amount=123.45"') from e

async def _get_currency_from_request(conn, request):
    currency_code = await _get_currency_code_from_request(request)
    currency = await db.get_currency_by_code(conn, currency_code)
    return currency

async def _fetch_currency(request):
    currency_code = await _get_currency_code_from_request(request)
    currency_rate = await request.app['currency_client'].get_currency_rate_by_code(currency_code)
    return currency_code, currency_rate

# GET /convert?from=BTC&to=EUR&amount=123.45
async def convert(request):
    _from, _to, _amount = await _get_convertion_args_from_request(request)
    async with request.app['db'].acquire() as conn:
        currency_from = await _get_currency_by_code(request, conn, _from)
        currency_to = await _get_currency_by_code(request, conn, _to)
        ret_value = (float(_amount) * currency_from['value']) / currency_to['value']
        return web.Response(text=str(ret_value))

async def _get_currency_by_code(request, conn, code):
    if code in request.app['cache']:
        currency = request.app['cache'][code]
        if datetime.now() - currency['last_update'] < timedelta(minutes=1):
            return currency
    currency = await db.get_currency_by_code(conn, code)
    if currency is None:
        raise web.HTTPBadRequest(text=code + ' is no registered')
    currency['last_update'] = datetime.now()
    request.app['cache'][code] = currency
    return currency




    
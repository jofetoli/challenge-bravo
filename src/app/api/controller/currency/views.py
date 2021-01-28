# app/api/controller/currency/views.py
from aiohttp import web
from datetime import datetime, timedelta
from psycopg2 import OperationalError

from infrastructure.db import update_currency, get_all_currency, get_currency_by_code, insert_currency
from model.amount import Amount


# GET /currency
async def index(request):
    try:
        async with request.app['db'].acquire() as conn:
            currencies = await get_all_currency(conn)
            return web.Response(text=str(currencies))
    except OperationalError:
        request.app['logger'].exception('index - error')
        return web.HTTPServiceUnavailable(text='Something went wrong while fetching the currencies')

# PUT /currency/:code
async def add_currency(request):
    try:
        async with request.app['db'].acquire() as conn:
            currency = await _get_currency_from_request(conn, request)
            if(currency == None):
                currency_code, currency_rate = await _fetch_currency(request) 
                currency = await insert_currency(conn, currency_code, currency_rate)
            elif currency['active'] == 0:
                currency['active'] = 1
                currency = await update_currency(conn, currency)
            return web.Response(text=str(currency))
    except OperationalError:
        request.app['logger'].exception('add_currency - error')
        return web.HTTPServiceUnavailable(text='Something went wrong while registering the currency')

# DELETE /currency/:code
async def rm_currency(request):
    try:
        async with request.app['db'].acquire() as conn:
            currency = await _get_currency_from_request(conn, request)
            if(currency == None or currency['active'] == 0):
                raise web.HTTPBadRequest(
                    text='You can\'t remove a not registered currency')

            currency['active'] = 0
            currency = await update_currency(conn, currency)
            request.app['cache'].delete(currency['code'])
            return web.Response(text=str(currency))
    except OperationalError:
        request.app['logger'].exception('rm_currency - error')
        return web.HTTPServiceUnavailable(text='Something went wrong while unregistering the currency')
    
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
    currency = await get_currency_by_code(conn, currency_code)
    return currency

async def _fetch_currency(request):
    currency_code = await _get_currency_code_from_request(request)
    currency_rate = await request.app['currency_client'].get_currency_rate_by_code(currency_code)
    return currency_code, currency_rate

# GET /convert?from=BTC&to=EUR&amount=123.45
async def convert(request):
    try:
        _from, _to, _amount = await _get_convertion_args_from_request(request)
        amount = Amount(_amount)
        async with request.app['db'].acquire() as conn:
            currency_from = await _get_currency_value_by_code(request, conn, _from)
            currency_to = await _get_currency_value_by_code(request, conn, _to)
            ret_value = (amount.value() * float(currency_to)) / float(currency_from)
            return web.Response(text=str(ret_value))
    except OperationalError:
        request.app['logger'].exception('convert - error')
        return web.HTTPServiceUnavailable(text='Something went wrong while converting the currency')
        

async def _get_currency_value_by_code(request, conn, code):
    currency_value = request.app['cache'].get(code)
    if currency_value is not None:
        return currency_value
    currency = await get_currency_by_code(conn, code)
    if currency is None:
        raise web.HTTPBadRequest(text=code + ' is not a registered currency')
    request.app['cache'].set(code, currency['value'])
    return currency['value']

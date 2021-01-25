"""
@package infrastructure.db
as this project only has an entity in its database everything related to db is in this module
"""
import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime, Boolean, Float
)
from datetime import datetime
from time import sleep
from psycopg2 import OperationalError
from infrastructure.logger import get_logger

meta = MetaData()
logger = get_logger('db')


"""
currency table information
"""
_currency = Table(
    'currency', meta,

    #Column('id', Integer, primary_key=True),
    Column('code', String(4), nullable=False),
    Column('value', Float, nullable=False),
    Column('active', Boolean, nullable=False),
    Column('last_update', DateTime, nullable=False)
)

async def init_pg(app):
    """
    init a db engine using the app configurations and store it in app['db']
    """
    logger.info('start db')
    conf = app['config']['postgres']
    for i in range(0, 5):
        try:
            engine = await aiopg.sa.create_engine(
                database=conf['database'],
                user=conf['user'],
                password=conf['password'],
                host=conf['host'],
                port=conf['port'],
                minsize=conf['minsize'],
                maxsize=conf['maxsize'],
            )
            break
        except OperationalError as e:
            if i >= 4:
                raise e
            sleep(1)
    app['db'] = engine

async def close_pg(app):
    """
    method created to be called when the app closes
    """
    logger.info('close db')
    app['db'].close()
    await app['db'].wait_closed()

async def get_all_currency(conn):
    """
    fetch all currencies active and registered currencies in the database
    """
    try:
        result = await conn.execute(
            _currency.select()
            .where(_currency.c.active))
        records = await result.fetchall()
        return [dict(c) for c in records]
    except Exception as e:
        logger.exception('get_all_currency - error')
        raise e


async def get_currency_by_code(conn, code):
    """
    fetch one registered currency by code
    """
    try:
        result = await conn.execute(
            _currency.select()
            .where(_currency.c.code == code))
        record = await result.first()
        return (record if (record is None) else dict(record.items()))
    except Exception as e:
        logger.exception('get_currency_by_code - error')
        raise e

async def insert_currency(conn, currency_code, currency_rate):
    """
    insert currency in the database
    """
    try:
        currency = {
            'code': currency_code,
            'value':currency_rate,
            'active':True,
            'last_update': datetime.now()
        }
        await conn.execute(
            _currency.insert(), currency
        )
        return currency
    except Exception as e:
        logger.exception('insert_currency - error')
        raise e

async def update_currency(conn, currency):
    """
    update currency in the database
    """
    try:
        currency['last_update'] = datetime.now()
        await conn.execute(
            _currency.update().where(_currency.c.code == currency['code']), currency
        )
        return currency
    except Exception as e:
        logger.exception('update_currency - error')
        raise e

#bravo/db.py
import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime, Boolean, Float
)
from datetime import datetime
from time import sleep
from psycopg2 import OperationalError 

meta = MetaData()

_currency = Table(
    'currency', meta,

    #Column('id', Integer, primary_key=True),
    Column('code', String(4), nullable=False),
    Column('value', Float, nullable=False),
    Column('active', Boolean, nullable=False),
    Column('last_update', DateTime, nullable=False)
)

_task_run = Table(
    'task_run', meta,

    #Column('id', Integer, primary_key=True),
    Column('name', String(200), nullable=False),
    Column('last_update', DateTime, nullable=False)
)

async def init_pg(app):
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
    app['db'].close()
    await app['db'].wait_closed()

async def get_all_currency(conn):
    result = await conn.execute(
        _currency.select()
        .where(_currency.c.active))
    records = await result.fetchall()
    return [dict(c) for c in records]

async def get_currency_by_code(conn, code):
    result = await conn.execute(
        _currency.select()
        .where(_currency.c.code == code))
    record = await result.first()
    return (record if (record is None) else dict(record.items()))

async def insert_currency(conn, currency_code, currency_rate):
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

async def update_currency(conn, currency):
    currency['last_update'] = datetime.now()
    await conn.execute(
        _currency.update().where(_currency.c.code == currency['code']), currency
    )
    return currency

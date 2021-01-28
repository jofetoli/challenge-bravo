#infrastructure/cache.py
from redis import Redis
from time import sleep

from infrastructure.logger import get_logger


logger = get_logger('redis')

def init_redis(config):
    """
    init a cache client using the app configurations
    """
    logger.info('start cache')
    config = config['redis']
    for i in range(0, 5):
        try:
            client = Redis(host=config['host'], port=config['port'])
            break
        except Exception as e:
            if i >= 4:
                raise e
            sleep(1)
    return client
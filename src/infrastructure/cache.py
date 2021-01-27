#infrastructure/cache.py
import redis

def init_redis(app):
    """
    init a cache client using the app configurations and store it in app['cache']
    """
    app['logger'].info('start cache')
    conf = app['config']['redis']
    for i in range(0, 5):
        try:
            client = redis.Redis(host=conf['host'], port=conf['port'])
            break
        except Exception as e:
            if i >= 4:
                raise e
            sleep(1)
    app['cache'] = client
from aiohttp import web
from decimal import Decimal

class Amount:

    _value = None
    
    def __init__(self, value_to_parse):
        try:
            value = Decimal(value_to_parse)
        except:
            raise web.HTTPBadRequest(
                text='Amount ({value}) is an invalid positive decimal. Use ''.'' for decimal separator'.format(value=value_to_parse))

        if not isinstance(value, Decimal) or value < 0:
            raise web.HTTPBadRequest(
                text='Amount ({value}) must be a positive decimal'.format(value=value))
        self._value = value

    def value(self):
        return float(self._value)
    
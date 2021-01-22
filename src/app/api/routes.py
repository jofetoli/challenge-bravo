# src/routes.py

from api.controller.currency.views import index, add_currency, rm_currency, convert

def setup_routes(app):
    app.router.add_get('/', index)

    app.router.add_post('/add_currency', add_currency, name='add_currency')
    app.router.add_post('/rm_currency', rm_currency, name='rm_currency')
    app.router.add_get('/convert', convert, name='convert')

# app/api/routes.py

from api.controller.currency.views import index, add_currency, rm_currency, convert

def setup_routes(app):
    app.router.add_get('/currency', index)

    app.router.add_put('/currency', add_currency, name='add_currency')
    app.router.add_delete('/currency', rm_currency, name='rm_currency')
    app.router.add_get('/currency/convert', convert, name='convert')

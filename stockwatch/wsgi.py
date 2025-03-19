"""
WSGI config for stockwatch project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockwatch.settings')

application = get_wsgi_application()

def before_first_request():
    from core.models import TickerSymbol
    from core.stockapi.polygon_client import PolygonClient
    try:
        print("refreshing ticker symbols")
        client = PolygonClient()

        data = client.get_tickers_snapshot(
            tickers=None,
            include_otc=False,
        )

        if 'tickers' in data:
            for ticker_data in data['tickers']:
                ticker_symbol = ticker_data.get('ticker')
                if ticker_symbol:
                    TickerSymbol.objects.get_or_create(ticker=ticker_symbol)
    except Exception as e:
        print(e)

before_first_request()
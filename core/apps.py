from django.apps import AppConfig

from core.stockapi.polygon_client import PolygonClient


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    # def ready(self):
    #     from core.models import TickerSymbol
    #     try:
    #         client = PolygonClient()
    #
    #         data = client.get_tickers_snapshot(
    #             tickers=None,
    #             include_otc=False,
    #         )
    #
    #         if 'tickers' in data:
    #             for ticker_data in data['tickers']:
    #                 ticker_symbol = ticker_data.get('ticker')
    #                 if ticker_symbol:
    #                     TickerSymbol.objects.get_or_create(ticker=ticker_symbol)
    #     except Exception as e:
    #         print(e)
from django.urls import path

from core.views.stock_views import *
from core.views.user_views import *
from core.views.watchlist_views import create_watchlist, add_ticker_to_watchlist, remove_ticker_from_watchlist, \
    get_user_watchlists, get_user_watchlist_by_id

urlpatterns = [
    # user & JWT
    path('register', register),
    path('login', login),
    path('refresh_token', refresh_access_token),
    path('logout', logout),
    # watchlist
    path('watchlists/create', create_watchlist),
    path('watchlists/all', get_user_watchlists),
    path('watchlists/<int:id>/add_ticker', add_ticker_to_watchlist),
    path('watchlists/remove_ticker', remove_ticker_from_watchlist),
    path('watchlists/<int:id>/', get_user_watchlist_by_id),

    # stock data
    path('search_tickers', get_search_tickers),
    path('stock_aggregate_data', get_stock_aggregate_data),
    path('stocks/details', get_ticker_details),
    path('tickers-snapshot', get_tickers_snapshot),
    path('news', get_news),
    # test
    path('user_info', get_user_info)
]
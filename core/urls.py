from django.urls import path
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

from core.views.stock_views import *
from core.views.user_views import *

urlpatterns = [
    # user & JWT
    path('register', register),
    path('login', login),
    path('refresh_token', refresh_access_token),
    path('logout', logout),
    # stock data
    path('search_tickers', get_search_tickers),
    path('stock_aggregate_data', get_stock_aggregate_data),
    path('ticker-details', get_ticker_details),
    path('tickers-snapshot', get_tickers_snapshot),
    path('get_ticker_list', get_ticker_list),
    # test
    path('user_info', get_user_info)
]
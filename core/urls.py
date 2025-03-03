from django.urls import path
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

from core import views

urlpatterns = [
    # user & JWT
    path('register', views.register_user),
    path('token_obtain_pair', views.token_obtain_pair),
    path('refresh_access_token', views.refresh_access_token),
    path('logout', views.logout),
    # stock data
    path('search_tickers', views.get_search_tickers),
    path('stock_aggregate_data', views.get_stock_aggregate_data),
    path('ticker-details', views.get_ticker_details),
    path('tickers-snapshot', views.get_tickers_snapshot),
    # test
    path('authenticated_request', views.authenticated_endpoint)
]
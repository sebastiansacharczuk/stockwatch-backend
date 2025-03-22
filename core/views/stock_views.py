from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from core.authentication import CookieJWTAuthentication
from core.models import TickerSymbol
from core.serializers import TickerSymbolSerializer
from core.stockapi.polygon_client import PolygonClient

@api_view(['GET'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_search_tickers(request):
    try:
        market = request.GET.get('market', 'stocks')
        search = request.GET.get('search', '')
        limit = int(request.GET.get('limit', 50))
        date = request.GET.get('date')
        ticker_type = request.GET.get('ticker_type')
        active = request.GET.get('active', 'true').lower() == 'true'


        client = PolygonClient()
        data = client.get_search_tickers(
            search=search,
            market=market,
            limit=limit,
            date=date,
            ticker_type=ticker_type,
            active=active
        )
        return JsonResponse({'status': 'success', 'data': data}, status=200)

    except ValueError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@api_view(['GET'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_stock_aggregate_data(request):
    try:
        ticker = request.GET.get('stockTicker')
        multiplier = request.GET.get('multiplier')
        timespan = request.GET.get('timespan')
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')
        adjusted = request.GET.get('adjusted', 'true').lower() == 'true'
        sort = request.GET.get('sort', 'asc')
        limit = int(request.GET.get('limit', 5000))

        if not all([ticker, multiplier, timespan, from_date, to_date]):
            print(ticker, multiplier, timespan, from_date, to_date)
            return JsonResponse({'status': 'error', 'message': 'Missing required parameters'}, status=400)

        multiplier = int(multiplier)
        client = PolygonClient()
        data = client.get_aggregate_data(
            ticker=ticker,
            multiplier=multiplier,
            timespan=timespan,
            from_date=from_date,
            to_date=to_date,
            adjusted=adjusted,
            sort=sort,
            limit=limit
        )
        return JsonResponse({'status': 'success', 'data': data}, status=200)

    except ValueError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@api_view(['GET'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_ticker_details(request):
    try:
        ticker = request.GET.get('ticker')
        date = request.GET.get('date')

        if not ticker:
            return JsonResponse({'status': 'error', 'message': 'Ticker is required'}, status=400)

        client = PolygonClient()
        data = client.get_ticker_details(
            ticker=ticker,
            date=date
        )
        return JsonResponse({'status': 'success', 'data': data}, status=200)

    except ValueError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'An unexpected error occurred',
            'details': str(e)
        }, status=500)

@api_view(['GET'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_tickers_snapshot(request):
    try:
        tickers = request.GET.get('tickers')
        include_otc = request.GET.get('include_otc', 'false').lower() == 'true'

        client = PolygonClient()
        ticker_list = tickers.split(',') if tickers else None

        data = client.get_tickers_snapshot(
            tickers=ticker_list,
            include_otc=include_otc
        )

        return JsonResponse({'status': 'success', 'data': data}, status=200)

    except ValueError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@api_view(['GET'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def refresh_tickers_db(request):
    try:
        tickers = request.GET.get('tickers')
        include_otc = request.GET.get('include_otc', 'false').lower() == 'true'

        client = PolygonClient()
        ticker_list = tickers.split(',') if tickers else None

        data = client.get_tickers_snapshot(
            tickers=ticker_list,
            include_otc=include_otc
        )

        if 'tickers' in data:
            for ticker_data in data['tickers']:
                ticker_symbol = ticker_data.get('ticker')
                if ticker_symbol:
                    TickerSymbol.objects.get_or_create(ticker=ticker_symbol)

        return JsonResponse({'status': 'success', 'data': data}, status=200)

    except ValueError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message':str(e)}, status=500)


@api_view(['GET'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_ticker_list(request):
    try:
        tickers = TickerSymbol.objects.all()
        serializer = TickerSymbolSerializer(tickers, many=True)
        return JsonResponse({'status': 'success', 'data': serializer.data}, status=200)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@api_view(['GET'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_news(request):
    try:
        ticker = request.GET.get('ticker', None)
        published_utc = request.GET.get('published_utc', None)
        order = request.GET.get('order', None)
        limit = request.GET.get('limit', '50')
        sort = request.GET.get('sort')

        client = PolygonClient()
        data = client.get_news(
            ticker= ticker,
            published_utc= published_utc,
            order= order,
            limit= int(limit),
            sort= sort
        )
        return JsonResponse({'status': 'success', 'data': data.get("results")}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

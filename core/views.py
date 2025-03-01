from django.http import JsonResponse
from .stockapi.polygon_client import PolygonClient


def get_search_tickers(request):
    try:
        market = request.GET.get('market', 'stocks')
        search = request.GET.get('search', '')
        limit = int(request.GET.get('limit', 100))
        date = request.GET.get('date')
        ticker_type = request.GET.get('type')
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
        return JsonResponse({
            'status': 'error',
            'message': 'An unexpected error occurred',
            'details': str(e)
        }, status=500)


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
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required parameters'
            }, status=400)

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
        return JsonResponse({
            'status': 'error',
            'message': 'An unexpected error occurred',
            'details': str(e)
        }, status=500)


def get_ticker_details(request):
    try:
        ticker = request.GET.get('ticker')
        date = request.GET.get('date')

        if not ticker:
            return JsonResponse({
                'status': 'error',
                'message': 'Ticker is required'
            }, status=400)

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
        return JsonResponse({
            'status': 'error',
            'message': 'An unexpected error occurred',
            'details': str(e)
        }, status=500)
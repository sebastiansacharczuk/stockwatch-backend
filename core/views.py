from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .serializers import UserRegistrationSerializer
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

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'message': 'User created successfully'}, status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_obtain_pair(request):
    serializer = TokenObtainPairSerializer(data=request.data)
    if serializer.is_valid():
        return JsonResponse(serializer.validated_data, status=200)
    return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def authenticated_endpoint(request):
    return JsonResponse({"status": "success"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_access_token(request):
    try:
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return JsonResponse({"status": "success", "message": "Refresh token is required"}, status=400)

        token = RefreshToken(refresh_token)
        new_access_token = token.access_token

        return JsonResponse({"status": "success", "access": new_access_token.__str__()},
            status=200
        )

    except Exception as e:
        return JsonResponse({"status": "success", "message": f"Logout failed: {str(e)}"}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return JsonResponse({"status": "success", "message": "Refresh token is required"}, status=400)

        token = RefreshToken(refresh_token)
        token.blacklist()
        return JsonResponse({"status": "success", "message": "Successfully logged out"}, status=205)
    except Exception as e:
        return JsonResponse({"status": "success", "message": f"Logout failed: {str(e)}"}, status=400)
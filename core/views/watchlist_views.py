from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from core.authentication import CookieJWTAuthentication
from core.models import Watchlist, WatchlistItem
from core.serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, WatchlistSerializer, \
    WatchlistItemSerializer


@api_view(['POST'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def create_watchlist(request):
    serializer = WatchlistSerializer(
        data=request.data,
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save(user=request.user)
        return JsonResponse({"status": "success", "data": serializer.data}, status=201)
    return JsonResponse({"status": "error", "errors": serializer.errors}, status=400)


@api_view(['POST'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def add_ticker_to_watchlist(request, id):
    try:
        watchlist = Watchlist.objects.get(id=id, user=request.user)
    except Watchlist.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Watchlista nie istnieje lub nie należy do użytkownika."}, status=404)

    serializer = WatchlistItemSerializer(data=request.data, context={'watchlist': watchlist})
    if serializer.is_valid():
        serializer.save(watchlist=watchlist)
        return JsonResponse({"status": "success", "data": serializer.data}, status=201)
    return JsonResponse({"status": "error", "errors": serializer.errors}, status=400)


@api_view(['DELETE'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def remove_ticker_from_watchlist(request, watchlist_id, ticker):
    try:
        watchlist = Watchlist.objects.get(id=watchlist_id, user=request.user)
        item = WatchlistItem.objects.get(watchlist=watchlist, ticker=ticker)
        item.delete()
        return JsonResponse({"status": "success", "message": "Ticker usunięty z watchlisty."}, status=204)
    except Watchlist.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Watchlista nie istnieje lub nie należy do użytkownika."},
                            status=404)
    except WatchlistItem.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Ticker nie istnieje w tej watchliście."}, status=404)


@api_view(['DELETE'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_watchlist(request, watchlist_id):
    try:
        watchlist = Watchlist.objects.get(id=watchlist_id, user=request.user)
        watchlist.delete()
        return JsonResponse({"status": "success", "message": "Watchlista została usunięta."}, status=204)
    except Watchlist.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Watchlista nie istnieje lub nie należy do użytkownika."},
                            status=404)


@api_view(['PUT'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def update_watchlist_name(request, watchlist_id):
    try:
        watchlist = Watchlist.objects.get(id=watchlist_id, user=request.user)
    except Watchlist.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Watchlista nie istnieje lub nie należy do użytkownika."},
                            status=404)

    serializer = WatchlistSerializer(watchlist, data=request.data, partial=True, context={'user': request.user})
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"status": "success", "data": serializer.data}, status=200)
    return JsonResponse({"status": "error", "errors": serializer.errors}, status=400)

@api_view(['GET'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_watchlists(request):
    watchlists = Watchlist.objects.filter(user=request.user)
    serializer = WatchlistSerializer(watchlists, many=True)
    return JsonResponse({"status": "success", "data": serializer.data}, status=200)

@api_view(['GET'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_watchlist_by_id(request, id):
    watchlists = Watchlist.objects.filter(user=request.user, id=id).first()
    serializer = WatchlistSerializer(watchlists, many=False)
    return JsonResponse({"status": "success", "data": serializer.data}, status=200)
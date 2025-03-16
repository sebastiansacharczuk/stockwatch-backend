from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from core.authentication import CookieJWTAuthentication
from core.serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'status': 'success'}, status=201)

    error_messages = []
    for key, messages in serializer.errors.items():
        error_messages.extend(messages)
    return JsonResponse({"status": "error", "errMsg": error_messages}, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = JsonResponse({'status': 'success'}, status=200)
        response.set_cookie(key="access_token", value=access_token, httponly=True, secure=False, samesite="Lax")
        response.set_cookie(key="refresh_token", value=str(refresh), httponly=True, secure=False, samesite="Lax")

        return response

    error_messages = []
    for key, messages in serializer.errors.items():
        error_messages.extend(messages)

    return JsonResponse({'status': 'error', 'errMsg': error_messages}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_access_token(request):
    try:
        refresh_token = request.COOKIES['refresh_token']

        if not refresh_token:
            return JsonResponse({"status": "error", "errMsg": "Refresh token is required"}, status=400)

        token = RefreshToken(refresh_token)
        new_access_token = token.access_token

        response = JsonResponse({"status": "success"}, status=200)
        response.set_cookie(key="access_token", value=str(new_access_token), httponly=True, secure=False, samesite="Lax")
        return response

    except Exception as e:
        print(e)
        return JsonResponse({"status": "error", "errMsg": str(e)}, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    try:
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            response = JsonResponse({"status": "error", "errMsg": "Refresh token not found."}, status=400)
        else:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
            response = JsonResponse({"status": "success"}, status=205)
    except Exception as e:
        response = JsonResponse({"status": "error", "errMsg": str(e)}, status=400)
    finally:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response



@api_view(['GET'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    return JsonResponse({"status": "success", "data": UserSerializer(request.user).data}, status=200)

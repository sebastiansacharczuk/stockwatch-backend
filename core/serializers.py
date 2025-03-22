from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.models import WatchlistItem, Watchlist, TickerSymbol

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            # Wywołaj oryginalną metodę validate
            return super().validate(attrs)
        except AuthenticationFailed as e:
            # Przekształć wyjątek AuthenticationFailed w ValidationError
            raise serializers.ValidationError(e.detail)

class WatchlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchlistItem
        fields = ['id', 'ticker']
        read_only_fields = ['id']

    def validate_ticker(self, value):
        watchlist = self.context.get('watchlist')
        if watchlist:
            qs = WatchlistItem.objects.filter(watchlist=watchlist, ticker=value)
            if self.instance:  # Przy aktualizacji pomijamy bieżącą instancję
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise serializers.ValidationError("Ten ticker już istnieje w tej watchliście.")
        return value

class WatchlistSerializer(serializers.ModelSerializer):
    items = WatchlistItemSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Watchlist
        fields = ['id', 'name', 'items', 'user']

    def validate_name(self, value):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            qs = Watchlist.objects.filter(user=user, name=value)
            if self.instance:  # Exclude current instance during update
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise serializers.ValidationError("Watchlista o tej nazwie już istnieje dla użytkownika.")
        return value


class TickerSymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = TickerSymbol
        fields = ['ticker']  # Only include the ticker field
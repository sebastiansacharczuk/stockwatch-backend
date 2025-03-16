from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlists')
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return f"{self.user.username}'s {self.name}"

class WatchlistItem(models.Model):
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name='items')
    ticker = models.CharField(max_length=10)

    class Meta:
        unique_together = ('watchlist', 'ticker')

    def __str__(self):
        return f"{self.ticker} in {self.watchlist.name}"

class TickerSymbol(models.Model):
    ticker = models.CharField(max_length=10, unique=True)  # Unique to avoid duplicates
    created_at = models.DateTimeField(auto_now_add=True)  # Optional: track when it was added

    def __str__(self):
        return self.ticker
import random
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

class Coin(models.Model):
    cryptoId = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256)
    symbol = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    currentPrice = models.FloatField(default=0)
    marketCap = models.FloatField(default=0)
    allTimeHigh = models.FloatField(default=0)
    allTimeLow = models.FloatField(default=0)
    dateCreated = models.DateField(null=True)
    image = models.CharField(max_length=256)
    priceHistory = models.JSONField(null=True)
    reportedBy = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.cryptoId

    def get_absolute_url(self):
        return reverse('coin_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        # Convert symbol to uppercase before saving
        self.symbol = self.symbol.upper()
        super().save(*args, **kwargs)

    def has_changed(self):
        if not self.pk:
            return True
        # Fetch the original values from the database
        original = Coin.objects.get(pk=self.pk)
        # Check if any of the specified fields have changed
        if (original.cryptoId != self.cryptoId or
                original.name != self.name or
                original.symbol != self.symbol or
                original.description != self.description or
                original.currentPrice != self.currentPrice or
                original.marketCap != self.marketCap or
                original.allTimeHigh != self.allTimeHigh or
                original.allTimeLow != self.allTimeLow or
                original.dateCreated != self.dateCreated or
                original.image != self.image):
            return True
        return False
    
    def formatted_current_price(self):
        return "${:,.2f}".format(self.currentPrice)

    def formatted_market_cap(self):
        return "${:,.2f}".format(self.marketCap)

    def formatted_all_time_high(self):
        return "${:,.2f}".format(self.allTimeHigh)

    def formatted_all_time_low(self):
        return "${:,.2f}".format(self.allTimeLow)

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Coin(models.Model):
    crypto_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    current_price = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    market_cap = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    ath = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    atl = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    date_created = models.DateField(null=True)
    image = models.CharField(max_length=256)
    price_history = models.JSONField(null=True)
    # reported_by = models.ForeignKey(
    #     get_user_model(), on_delete=models.CASCADE, null=True, blank=True
    # )

    def __str__(self):
        return self.crypto_id

    def get_absolute_url(self):
        return reverse('coin_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.symbol = self.symbol.upper()
        super().save(*args, **kwargs)

    def has_changed(self):
        if not self.pk:
            return True
        for field in ['crypto_id', 'name', 'symbol', 'description', 'current_price',
                      'market_cap', 'ath', 'atl', 'date_created', 'image']:
            if getattr(self, field) != getattr(self.__class__.objects.get(pk=self.pk), field):
                return True
        return False
    
    def formatted_current_price(self):
        return "${:,.2f}".format(self.current_price)

    def formatted_market_cap(self):
        return "${:,.2f}".format(self.market_cap)

    def formatted_all_time_high(self):
        return "${:,.2f}".format(self.ath)

    def formatted_all_time_low(self):
        return "${:,.2f}".format(self.atl)


class Bitcoin(models.Model):
    sno = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    date = models.DateTimeField()
    high = models.FloatField()
    low = models.FloatField()
    open = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    market_cap = models.FloatField()

    def __str__(self):
        return str(self.sno)
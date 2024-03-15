from rest_framework import serializers
from .models import Coin,Bitcoin


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = "__all__"

class BitcoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bitcoin
        fields = "__all__"

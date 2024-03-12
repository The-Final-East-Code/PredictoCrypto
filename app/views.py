from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import Coin
from .permissions import IsOwnerOrReadOnly
from .serializers import CoinSerializer


class CoinList(ListCreateAPIView):
    queryset =Coin.objects.all()
    serializer_class = CoinSerializer


class CoinDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer

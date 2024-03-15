import io
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import Coin
from .permissions import IsOwnerOrReadOnly
from .serializers import CoinSerializer

from django.shortcuts import render
from django.http import HttpResponse
from .views_front import UploadFileForm
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from .tools.analyze_crypto import plot_graph


class CoinList(ListCreateAPIView):
    queryset =Coin.objects.all()
    serializer_class = CoinSerializer


class CoinDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer

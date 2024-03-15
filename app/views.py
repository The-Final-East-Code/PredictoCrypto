import io
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import Coin
from .permissions import IsOwnerOrReadOnly
from .serializers import CoinSerializer

from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from .views_front import UploadFileForm
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from .tools.analyze_crypto import plot_graph
from .models import Coin, CsvUploads, PlotImages


class CoinList(ListCreateAPIView):
    queryset =Coin.objects.all()
    serializer_class = CoinSerializer


class CoinDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer


# views.py or views_front.py
class PlotImageView(View):
    def get(self, request, pk):
        user_plot = PlotImages.objects.get(pk=pk, user=request.user)  # Ensure the plot belongs to the user
        context = {'plot_image_path': user_plot.path.url if user_plot else None}
        return render(request, 'coin/plot_display.html', context)
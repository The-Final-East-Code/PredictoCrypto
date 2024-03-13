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
from .analyze_crypto import plot_graph


class CoinList(ListCreateAPIView):
    queryset =Coin.objects.all()
    serializer_class = CoinSerializer


class CoinDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer


# def upload_and_plot(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Process the uploaded file
#             file = request.FILES['file']
#             fig = plot_graph(file)  # Ensure your plot_graph function returns a matplotlib Figure object
#             response = HttpResponse(content_type='image/png')
#             canvas = FigureCanvas(fig)
#             canvas.print_png(response)
#             return response
#     else:
#         form = UploadFileForm()
#     return render(request, 'your_template.html', {'form': form})
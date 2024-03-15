from django.urls import path
from .views import CoinList, CoinDetail, PlotImageView

urlpatterns = [
    path("", CoinList.as_view(), name="coin_list"),
    path("<int:pk>/", CoinDetail.as_view(), name="coin_detail"),
    path('plot-image/', PlotImageView.as_view(), name='plot_image'),
]

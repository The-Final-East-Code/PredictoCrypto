from django.urls import path
from .views import CoinList, CoinDetail

urlpatterns = [
    path("", CoinList.as_view(), name="coin_list"),
    path("<int:pk>/", CoinDetail.as_view(), name="coin_detail"),
]

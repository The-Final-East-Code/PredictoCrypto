from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import CoinList, CoinDetail

urlpatterns = [
    path("", CoinList.as_view(), name="coin_list"),
    path("<int:pk>/", CoinDetail.as_view(), name="coin_detail"),
]

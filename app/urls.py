from django.urls import path
from .views import CoinList, CoinDetail
from .views_front import CoinTop20View

urlpatterns = [
    path("", CoinList.as_view(), name="coin_list"),
    path("<int:pk>/", CoinDetail.as_view(), name="coin_detail"),
    path("coin_top_20/", CoinTop20View.as_view(), name="coin_top_20"),
]

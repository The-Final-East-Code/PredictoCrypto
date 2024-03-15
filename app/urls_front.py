from django.urls import path
from .views_front import (
    CoinCreateView,
    CoinDeleteView,
    CoinDetailView,
    CoinListView,
    CoinUpdateView,
    FileUploadView,
    CoinTop20View,
    CoinTop20View,)

urlpatterns = [
    path("", CoinListView.as_view(), name="coin_list"),
    path("<int:pk>/", CoinDetailView.as_view(), name="coin_detail"),
    path("create/", CoinCreateView.as_view(), name="coin_create"),
    path("<int:pk>/update/", CoinUpdateView.as_view(), name="coin_update"),
    path("<int:pk>/delete/", CoinDeleteView.as_view(), name="coin_delete"),
    path("upload/", FileUploadView.as_view(), name="coin_upload"),
    path("coin_top_20/", CoinTop20View.as_view(), name="coin_top_20"),
]

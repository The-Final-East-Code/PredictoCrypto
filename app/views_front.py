from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Coin


class CoinListView(LoginRequiredMixin, ListView):
    template_name = "coin/coin_list.html"
    model = Coin
    context_object_name = "coin"


class CoinDetailView(LoginRequiredMixin, DetailView):
    template_name = "coin/coin_detail.html"
    model = Coin
    context_object_name = "coin"


class CoinUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "coin/coin_update.html"
    model = Coin
    context_object_name = "coin"
    fields = [
        "cryptoId", "name", "symbol", "description",
        "currentPrice", "marketCap", "allTimeHigh",
        "allTimeLow", "dateCreated", "image", "priceHistory", "reportedBy"
        ] # OR "__all__" for all of them


class CoinCreateView(LoginRequiredMixin, CreateView):
    template_name = "coin/coin_create.html"
    model = Coin
    fields = [
        "cryptoId", "name", "symbol", "description",
        "currentPrice", "marketCap", "allTimeHigh",
        "allTimeLow", "dateCreated", "image", "priceHistory", "reportedBy"
        ] # OR "__all__" for all of them


class CoinDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "coin/coin_delete.html"
    model = Coin
    success_url = reverse_lazy("coin_list")

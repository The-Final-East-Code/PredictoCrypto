from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from .analyze_crypto import plot_graph
from django.urls import reverse_lazy
from .forms import UploadFileForm
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
    fields = "__all__"
    # fields = [
    #     "crypto_id", "name", "symbol", "description",
    #     "current_price", "market_cap", "ath",
    #     "atl", "date_created", "image", "price_history", "reported_by"
    #     ]


class CoinCreateView(LoginRequiredMixin, CreateView):
    template_name = "coin/coin_create.html"
    model = Coin
    fields = "__all__"
    # fields = [
    #     "crypto_id", "name", "symbol", "description",
    #     "current_price", "market_cap", "ath",
    #     "atl", "date_created", "image", "price_history", "reported_by"
    #     ] # OR "__all__" for all of them


class CoinDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "coin/coin_delete.html"
    model = Coin
    success_url = reverse_lazy("coin_list")


class FileUploadView(LoginRequiredMixin, FormView):
    template_name = "coin/coin_upload.html"
    form_class = UploadFileForm
    success_url = reverse_lazy('coin_list')  # Change to your actual success URL name

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        file = form.cleaned_data['file']
        result = plot_graph(file) # Assume this function accepts a file-like object and returns a matplotlib figure

        # If plot_graph returns a tuple, assume the first element is the figure we want
        fig = result[0] if isinstance(result, tuple) else result

        # Create an HTTP response with a plot image
        response = HttpResponse(content_type='image/png')
        canvas = FigureCanvas(fig)
        canvas.print_png(response)
        return response

    def form_invalid(self, form):
        # Optional: Handle cases where the form is not valid
        return super().form_invalid(form)
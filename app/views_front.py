import os
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView, TemplateView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.timezone import now
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from .analyze_crypto import plot_graph
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

class CoinCreateView(LoginRequiredMixin, CreateView):
    template_name = "coin/coin_create.html"
    model = Coin
    fields = "__all__"

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

        # Ensure the uploads directory exists
        uploads_dir = os.path.join(settings.BASE_DIR, 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)

        # Generate a unique filename for the plot
        timestamp = now().strftime('%Y%m%d%H%M%S')  # Current time as a string
        filename = f"plot_{timestamp}.png"
        filepath = os.path.join(uploads_dir, filename)

        # Save the figure to the specified file path
        fig.savefig(filepath)

        # Create an HTTP response with a plot image
        response = HttpResponse(content_type='image/png')

class CoinTop20View(LoginRequiredMixin,ListView):
    template_name = "coin_top_20.html"
    model = Coin
    context_object_name = "coins"

    def get_queryset(self):
        # Return the top 20 coins here based on your criteria
        return Coin.objects.order_by('-market_cap')[:20]
import os
import random
import requests
import csv
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView, TemplateView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.urls import reverse, reverse_lazy
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from .forms import UploadFileForm
from .models import Coin
from .tools.ai_run import chat_with_openai
from .tools.analyze_crypto import plot_graph,summarize_data,call_cgpt_api
from .tools.random_youtube_vid import get_youtube_vid_ids


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
    fields = "__all__" # "__all__" for all of them
    # or fields = [ "crypto_id", "name", "symbol",... ] 

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
    success_url = reverse_lazy('coin_list')

    def form_valid(self, form):
        # Called when valid form data has been POSTed
        # Returns an HttpResponse
        file = form.cleaned_data['file']
        filename = file.name

        # Determine file type and process accordingly
        if filename.endswith('.csv'):
            plot = plot_graph(file)
            # Ensure the uploads directory exists
            uploads_dir = os.path.join(settings.BASE_DIR, 'static', 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)

            # Generate a unique filename for the plot
            timestamp = now().strftime('%Y%m%d%H%M%S')
            filename = f"plot_{timestamp}.png"
            filepath = os.path.join(uploads_dir, filename)

            # If tuple is returned, get the first element as figure
            fig = plot[0] if isinstance(plot, tuple) else plot
            # Save the figure to the specified file path
            fig.savefig(filepath)
            # Create an HTTP response with a plot image
            response = HttpResponse(content_type='image/png')
            canvas = FigureCanvas(fig)
            canvas.print_png(response)
            return response
            # Display the response directly
            # return HttpResponse(response)
        else:
            # File type not supported
            return HttpResponse("Unsupported file type.", status=400)

    def form_invalid(self, form):
        # Optional: Handle case where form is not valid
        return super().form_invalid(form)

# View to handle chat requests
class ChatView(LoginRequiredMixin, TemplateView):
    template_name = "coin/ai_chat.html"

# @method_decorator(csrf_exempt, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class ChatPostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user_message = data.get('message', '')
        response_message = chat_with_openai(user_message)
        return JsonResponse({'response': response_message})

class CoinTop20View(LoginRequiredMixin,ListView):
    template_name = "coin_top_20.html"
    model = Coin
    context_object_name = "coins"

    def get_queryset(self):
        # Return the top 20 coins here based on your criteria
        return Coin.objects.order_by('id')[:20]

class LearnView(LoginRequiredMixin, TemplateView):
    template_name = "coin/learn.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # List of cryptocurrency-related YouTube video IDs
        video_ids = get_youtube_vid_ids("cryptocurrency")
        selected_video_id = random.choice(video_ids)
        context['video_id'] = selected_video_id
        return context
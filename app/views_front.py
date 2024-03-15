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
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView, TemplateView
from django.urls import reverse_lazy
from django.utils.timezone import now
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from .forms import UploadFileForm
from .models import Coin, CsvUploads, PlotImages
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
    success_url = reverse_lazy('coin_list')  # Adjust as needed

    def form_valid(self, form):
        user = self.request.user
        file = form.cleaned_data['file']
        filename = file.name
        description = form.cleaned_data.get('description', '')

        # Ensure the directory for CSVs exists under MEDIA_ROOT/csv
        csv_dir = os.path.join(settings.MEDIA_ROOT, 'csv')
        os.makedirs(csv_dir, exist_ok=True)
        
        # Include the user's ID in the file name to ensure uniqueness
        user_id_str = f"user_{user.id}_"
        csv_filename = user_id_str + now().strftime('%Y%m%d%H%M%S_') + filename
        csv_file_path = os.path.join(csv_dir, csv_filename)

        # Save the CSV file
        with open(csv_file_path, 'wb+') as csv_file:
            for chunk in file.chunks():
                csv_file.write(chunk)

        # Save CSV upload information to the database
        CsvUploads.objects.create(
            user=user,
            path=os.path.join('csv', csv_filename),  # Store relative path
            description=description,
            coin=None  # Placeholder, adjust as needed
        )

        # Process the CSV if it's the correct format
        if filename.endswith('.csv'):
            plot = plot_graph(csv_file_path)  # Adjust plot_graph to use file path

            # Ensure the directory for plots exists under MEDIA_ROOT/plots
            plot_dir = os.path.join(settings.MEDIA_ROOT, 'plots')
            os.makedirs(plot_dir, exist_ok=True)

            plot_filename = user_id_str + now().strftime('%Y%m%d%H%M%S_plot.png')
            plot_file_path = os.path.join(plot_dir, plot_filename)

            # Assuming `plot` is a Matplotlib figure, or you have logic to handle the plot object
            fig = plot[1] if isinstance(plot, tuple) else plot
            fig.savefig(plot_file_path)

            # Save plot image information to the database
            PlotImages.objects.create(
                user=user,
                path=os.path.join('plots', plot_filename),  # Store relative path
                description=f"Plot generated from {filename}",
                coin=None  # Placeholder, adjust as needed
            )

            # Optionally, store plot information in session or redirect to a view that displays the plot
            # self.request.session['plot_image_path'] = plot_file_path
            # Adjust redirection or response as needed
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponse("Unsupported file type.", status=400)

    def form_invalid(self, form):
        # Handle case where form is not valid
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
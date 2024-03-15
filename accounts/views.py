from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserEditForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserEditForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
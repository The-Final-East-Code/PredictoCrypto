from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserEditForm(CustomUserChangeForm):
    class Meta(CustomUserChangeForm.Meta):
        fields = CustomUserChangeForm.Meta.fields + ('bio', 'profile_picture',)
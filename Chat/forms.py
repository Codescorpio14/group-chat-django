from turtle import clear
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Rooms, User


class RoomForm(forms.ModelForm):
    class Meta:
        model = Rooms
        fields = ["name", "topic", "description"]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "avatar",
            "name",
            "username",
            "email",
            "bio",
        ]


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "name"]

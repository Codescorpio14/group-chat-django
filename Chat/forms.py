from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Rooms


class RoomForm(ModelForm):
    class Meta:
        model = Rooms
        fields = ["name", "topic", "description"]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
        ]

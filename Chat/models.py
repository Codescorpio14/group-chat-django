from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, default="avatar.svg")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Topics(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Rooms(models.Model):
    topic = models.ForeignKey(Topics, on_delete=models.SET_NULL, null=True)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[0:50]

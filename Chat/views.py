from pydoc_data import topics
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Rooms, Topics, Message
from django.contrib.auth.models import User
from .forms import RoomForm

# Create your views here.


def home(request):
    return redirect("rooms")


def rooms(request):
    topic = request.GET.get("topic") if request.GET.get("topic") != None else ""
    rooms = Rooms.objects.filter(
        Q(topic__name__icontains=topic)
        | Q(name__contains=topic)
        | Q(host__username__icontains=topic),
    )
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=topic)
    ).order_by("-created_at", "-updated_at")[:6]

    topics = Topics.objects.all()
    return render(
        request,
        "chat/rooms.html",
        {"rooms": rooms, "topics": topics, "room_messages": room_messages},
    )


def singleRoomView(request, id):
    room = Rooms.objects.get(id=id)
    room_messages = room.message_set.all().order_by("created_at")
    room_participants = room.participants.all()

    if request.method == "POST":
        content = request.POST.get("content")
        if content != "":
            message = Message.objects.create(
                user=request.user,
                room=room,
                content=request.POST.get("content"),
            )
            room.participants.add(request.user)
            return redirect("room", id=id)
        else:
            return HttpResponse("Message cannot be empty")

    return render(
        request,
        "chat/single_room.html",
        {
            "room": room,
            "room_messages": room_messages,
            "room_participants": room_participants,
        },
    )


@login_required(login_url="login")
def delete_message(request, id):
    message = Message.objects.get(id=id)
    if request.user != message.user:
        return HttpResponse("You are not allowed to delete this.")
    if request.method == "POST":
        message.delete()
        return redirect("room", id=message.room.id)
    return render(request, "chat/delete.html", {"obj": message})


def edit_message(request, id):
    message = Message.objects.get(id=id)
    if request.user != message.user:
        return HttpResponse("You are not allowed to edit this.")
    if request.method == "POST":
        message.content = request.POST.get("content")
        message.save()
        return redirect("room", id=message.room.id)
    return render(request, "chat/edit.html", {"message": message})


@login_required(login_url="login")
def create_room(request):
    form = RoomForm()

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect("rooms")
    return render(request, "chat/room_form.html", {"form": form})


@login_required(login_url="login")
def update_room(request, id):
    room = Rooms.objects.get(id=id)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed to update this.")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("rooms")

    return render(request, "chat/room_form.html", {"form": form})


@login_required(login_url="login")
def delete_room(request, id):
    room = Rooms.objects.get(id=id)

    if request.user != room.host:
        return HttpResponse("You are not allowed to delete this.")

    if request.method == "POST":
        room.delete()
        return redirect("rooms")
    return render(request, "chat/delete.html", {"room": room})


def register_user(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "There was an error during registration")
    return render(request, "user/login_register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password does not exist")
    return render(request, "user/login_register.html")


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required(login_url="login")
def user_profile(request, id):
    user = User.objects.get(id=id)
    rooms = user.rooms_set.all()
    user_activities = user.message_set.all()
    topics = Topics.objects.all()
    return render(
        request,
        "user/profile.html",
        {
            "user": user,
            "rooms": rooms,
            "room_messages": user_activities,
            "topics": topics,
        },
    )

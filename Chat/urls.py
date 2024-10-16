from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # Room Curd Urls
    path("rooms/", views.rooms, name="rooms"),
    path("rooms/<str:id>", views.singleRoomView, name="room"),
    path("rooms/create/", views.create_room, name="create-room"),
    path("rooms/update/<str:id>/", views.update_room, name="update-room"),
    path("rooms/delete/<str:id>/", views.delete_room, name="delete-room"),
    # Message Curd Urls
    path("rooms/delete-message/<str:id>/", views.delete_message, name="delete-message"),
    path("rooms/edit-message/<str:id>/", views.edit_message, name="edit-message"),
    # User Auth Urls
    path("user/register/", views.register_user, name="register"),
    path("user/login/", views.login_view, name="login"),
    path("user/logout/", views.logout_view, name="logout"),
    path("user/profile/<str:id>/", views.user_profile, name="profile"),
]

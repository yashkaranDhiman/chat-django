from django.urls import path
from base import views

urlpatterns = [
    path("",views.home,name="homepage"),
    path("login/",views.login_user,name="login"),
    path("register/",views.registerUser,name="register"),

    path("logout/",views.logout_user,name="logout"),
    path("room/<str:pk>/",views.room,name="room"),
    path("create-room/",views.createRoom,name="create-room"),
    path("friends/",views.friends,name="friends"),
    path("user-profile/<str:pk>/",views.userProfile,name="user-profile"),

    path("update-room/<str:pk>/",views.roomUpdate,name="update-room"),
    path("delete-room/<str:pk>/",views.deleteRoom,name="delete-room"),
    path("delete-comment/<str:pk>/",views.deleteComment,name="delete-comment"),
]
 
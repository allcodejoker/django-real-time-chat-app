from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name="index"),
   path('register_user/', views.register_user, name="register_user"),
   path('login_user/', views.login_user, name="login_user"),
   path('logout_user/', views.logout_user, name="logout_user"),
   path('chat/<str:room_code>/', views.chat_room, name="chat_room"),
   path('find_room/', views.find_room, name="find_room"),
   path('create_room/', views.create_room, name="create_room"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.chat_page, name="chat_page"),
    path("chat/<int:user_id>/", views.private_chat, name="chat_with_user"),

]

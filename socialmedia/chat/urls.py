# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.chat_page, name="chat_page"),
    path("chat/<int:user_id>/", views.private_chat, name="chat_with_user"),
    path("mark-read/<int:user_id>/", views.mark_messages_read, name="mark_messages_read"),
]
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Message
from django.http import JsonResponse
# from django.db import models
from django.db.models import Q

@login_required(login_url='login')
def chat_page(request):
    User = get_user_model()
    users = User.objects.exclude(id=request.user.id)  # باش مايبانش راسو
    return render(request, "chat/chat.html", {"users": users})

@login_required(login_url='login')
def private_chat(request, user_id):
    
    User = get_user_model()
    other_user = User.objects.get(id=user_id)
    users = User.objects.exclude(id=request.user.id)
    
    return render(request, "chat/chat.html", {
        "other_user": other_user,
        "users": users
    })

# In your views.py
def get_messages(request, user_id):
    messages = Message.objects.filter(
        Q(sender=request.user, receiver_id=user_id) |
        Q(sender_id=user_id, receiver=request.user)
    ).order_by('timestamp')
    
    return JsonResponse([{
        'content': msg.content,
        'sender': msg.sender.username,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for msg in messages], safe=False)

from django.shortcuts import render

def ws_test(request):
    return render(request, "test.html")

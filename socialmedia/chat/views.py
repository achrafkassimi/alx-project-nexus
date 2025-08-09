# chat/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Message
from django.http import JsonResponse
from django.db.models import Q, Count, Case, When, IntegerField
from django.db.models.functions import Coalesce

@login_required(login_url='login')
def chat_page(request):
    User = get_user_model()
    
    # Get all users except current user with unread message counts
    users_with_unread = []
    for user in User.objects.exclude(id=request.user.id):
        unread_count = Message.objects.filter(
            sender=user,
            receiver=request.user,
            is_read=False
        ).count()
        
        users_with_unread.append({
            'user': user,
            'unread_count': unread_count
        })
    
    return render(request, "chat/chat.html", {
        "users_with_unread": users_with_unread
    })

@login_required(login_url='login')
def private_chat(request, user_id):
    User = get_user_model()
    other_user = get_object_or_404(User, id=user_id)
    
    # Mark all messages from this user as read
    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)
    
    # Get all users with unread counts
    users_with_unread = []
    for user in User.objects.exclude(id=request.user.id):
        unread_count = Message.objects.filter(
            sender=user,
            receiver=request.user,
            is_read=False
        ).count()
        
        users_with_unread.append({
            'user': user,
            'unread_count': unread_count
        })
    
    return render(request, "chat/chat.html", {
        "other_user": other_user,
        "users_with_unread": users_with_unread
    })

@login_required
def mark_messages_read(request, user_id):
    """API endpoint to mark messages as read"""
    if request.method == 'POST':
        Message.objects.filter(
            sender_id=user_id,
            receiver=request.user,
            is_read=False
        ).update(is_read=True)
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'})

# Keep existing functions
def get_messages(request, user_id):
    messages = Message.objects.filter(
        Q(sender=request.user, receiver_id=user_id) |
        Q(sender_id=user_id, receiver=request.user)
    ).order_by('timestamp')
    
    return JsonResponse([{
        'content': msg.content,
        'sender': msg.sender.username,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'is_read': msg.is_read
    } for msg in messages], safe=False)

def ws_test(request):
    return render(request, "test.html")
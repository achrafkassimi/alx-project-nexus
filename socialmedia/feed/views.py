from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post  # تأكد من أن عندك Post model

@login_required
def dashboard_view(request):
    user = request.user
    posts = Post.objects.all().order_by('-created_at')  # أحدث المنشورات أولاً

    context = {
        'user': user,
        'posts': posts,
    }
    return render(request, 'feed/dashboard.html', context)

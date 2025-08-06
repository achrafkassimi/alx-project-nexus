from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post
from django.db.models import Q

@login_required(login_url='login')
def dashboard_view(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(content__icontains=query) | Q(author__username__icontains=query)
        ).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    
    context = {'posts': posts}
    return render(request, 'feed/dashboard.html', context)

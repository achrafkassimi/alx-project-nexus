from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
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


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.liked_by.all():
        post.liked_by.remove(user)
    else:
        post.liked_by.add(user)

    return redirect('feed:dashboard')


@login_required(login_url='login')
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('feed:dashboard')


@login_required(login_url='login')
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        content = request.POST.get('content')
        post.content = content
        post.save()
        return redirect('feed:dashboard')

    return render(request, 'feed/edit_post.html', {'post': post})


@login_required(login_url='login')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return redirect('feed:dashboard')


@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # فقط صاحب التعليق يقدر يحذفه
    if request.user == comment.author:
        comment.delete()

    return redirect('feed:dashboard')

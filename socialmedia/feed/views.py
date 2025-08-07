from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.db.models import Q
from django.http import JsonResponse

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

# @login_required(login_url='login')
# def like_post(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     user = request.user

#     if user in post.liked_by.all():
#         post.liked_by.remove(user)
#     else:
#         post.liked_by.add(user)

#     return redirect('feed:dashboard')

@login_required(login_url='login')
def toggle_like(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(pk=post_id)
        user = request.user

        if user in post.liked_by.all():
            post.liked_by.remove(user)
            liked_by = False
        else:
            post.liked_by.add(user)
            liked_by = True

        return JsonResponse({
            'liked_by': liked_by,
            'total_likes': post.liked_by.count()
        })
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required(login_url='login')
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('feed:dashboard')


# @login_required(login_url='login')
# def edit_post(request, post_id):
#     post = get_object_or_404(Post, id=post_id, author=request.user)

#     if request.method == 'POST':
#         content = request.POST.get('content')
#         post.content = content
#         post.save()
#         return redirect('feed:dashboard')

#     return render(request, 'feed/edit_post.html', {'post': post})


# @login_required(login_url='login')
# def delete_post(request, post_id):
#     post = get_object_or_404(Post, id=post_id, author=request.user)
#     post.delete()
#     return redirect('feed:dashboard')


@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # فقط صاحب التعليق يقدر يحذفه
    if request.user == comment.author:
        comment.delete()

    return redirect('feed:dashboard')


@login_required(login_url='login')
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # فقط صاحب التعليق يقدر يحررو
    if request.user != comment.author:
        return redirect('feed:dashboard')

    if request.method == 'POST':
        new_content = request.POST.get('content')
        if new_content:
            comment.content = new_content
            comment.save()
            return redirect('feed:dashboard')

    return render(request, 'feed/edit_comment.html', {'comment': comment})


# feed/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('feed:dashboard')
    else:
        form = PostForm()
    
    return render(request, 'feed/create_post.html', {'form': form})


from django.shortcuts import get_object_or_404

@login_required(login_url='login')
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('feed:dashboard')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('feed:dashboard')
    else:
        form = PostForm(instance=post)

    return render(request, 'feed/edit_post.html', {'form': form, 'post': post})


@login_required(login_url='login')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author == request.user:
        post.delete()

    return redirect('feed:dashboard')


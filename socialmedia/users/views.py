from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from feed.models import Post


def register_view(request):
    if request.user.is_authenticated:
        return redirect('feed:dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            print(f"User {username} registered successfully with password: {raw_password}")  # Debugging line
            # Authenticate the user after registration
            user = authenticate(request, username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Registration successful! Welcome, {user.username} 🎉")
                return redirect('feed:dashboard')
            else:
                messages.error(request, "Authentication failed after registration.")
        else:
            messages.error(request, "There was an error during registration.")
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed:dashboard')  # ولا أي صفحة بغيتي توصل ليها
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}! 🎉")
            return redirect('feed:dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('users:login')


@login_required(login_url='login')
def profile_view(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-created_at')

    context = {
        'profile_user': user,
        'posts': posts,
    }
    return render(request, 'users/profile.html', context)

@login_required(login_url='login')
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('users:profile')
    return render(request, 'users/confirm_delete.html', {'post': post})
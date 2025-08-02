from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm
from django.contrib import messages



def register_view(request):
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

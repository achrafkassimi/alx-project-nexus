from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

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


from django.shortcuts import render

def ws_test(request):
    return render(request, "test.html")

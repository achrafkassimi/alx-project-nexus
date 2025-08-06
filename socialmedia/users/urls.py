from django.urls import path
from .views import register_view, login_view, logout_view
from .views import profile_view, delete_post_view


app_name = 'users'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('profile/', profile_view, name='profile'),
    path('post/<int:post_id>/delete/', delete_post_view, name='delete_post'),

]

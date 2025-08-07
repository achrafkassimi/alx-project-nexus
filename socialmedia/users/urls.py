from django.urls import path
from .views import register_view, login_view, logout_view
from .views import profile_view, delete_post_view,edit_profile
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


app_name = 'users'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('profile/', profile_view, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),

    path('post/<int:post_id>/delete/', delete_post_view, name='delete_post'),

    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='users/change_password.html',
        success_url=reverse_lazy('users:password_change_done')
    ), name='change_password'),

    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'
    ), name='password_change_done'),
]

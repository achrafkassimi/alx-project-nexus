from django.urls import path
from . import views

app_name = 'feed'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # path('', views.dashboard_view, name='dashboard'),  # Redirect to dashboard
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),

]

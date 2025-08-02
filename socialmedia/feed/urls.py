from django.urls import path
from . import views

app_name = 'feed'  # 👈 مهم جدا لتفعيل namespace

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # زيد هنا أي route أخرى: post, like, comment...
]

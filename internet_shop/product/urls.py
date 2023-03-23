from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import login_view, register_view

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:id>/', views.product_detail, name='product_detail'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/register/', register_view, name='register'),
    path('accounts/logout/', LogoutView.as_view(next_page='product_list'), name='logout'),
]

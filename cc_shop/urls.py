from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('profile/', views.profile, name='profile'),
    path('products/', views.list_products, name='list_products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('purchase_confirmation/', views.purchase_confirmation, name='purchase_confirmation'),
    path('impact/', views.impact, name='impact'),
]
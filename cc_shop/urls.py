from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html', next_page=reverse_lazy('dashboard')), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('logout_page')), name='logout'),
    path('register/', views.register, name='register'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('products/', views.list_products, name='list_products'),
    path('products/<str:product_id>/', views.product_detail, name='product_detail'),
    path('products/purchase/<int:product_id>/', views.purchase_product, name='purchase_product'),
    path('products/complete_purchase/<int:product_id>/', views.complete_purchase, name='complete_purchase'),
    path('purchase_confirmation/', views.purchase_confirmation, name='purchase_confirmation'),
    path('impact/', views.impact, name='impact'),
    path('cart/add/<str:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('logout_page/', views.logout_page, name='logout_page'),
]
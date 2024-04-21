from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, reverse_lazy
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('impact/', views.impact, name='impact'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html', next_page=reverse_lazy('dashboard')), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('logout_page')), name='logout'),
    path('logout_page/', views.logout_page, name='logout_page'),
    
    # Products urls
    path('products/', views.list_products, name='list_products'),
    path('products/<str:product_id>/', views.product_detail, name='product_detail'),

    # Payment urls
    path('make_payment/', views.make_payment, name='make_payment'),
    path('payment_status/', views.payment_status, name='payment_status'),

    # Cart urls
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<str:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),

    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Admin product management URLs
    path('management/products/', views.product_list, name='product_list'),
    path('management/products/add/', views.add_product, name='add_product'),
    path('management/products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('management/products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
]
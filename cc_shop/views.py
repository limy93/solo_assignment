from datetime import datetime
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, DecimalField, F, Sum
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import LoginForm, ProductForm, RegisterForm
from .models import Cart, CartItem, ElectricConsumption, Product, Purchase, User

def home(request):
    return render(request, 'home.html')

def about(request):
    """Render the about page."""
    return render(request, 'about.html')

def impact(request):
    # Example data fetching and aggregation
    total_co2_reduction = 10000   # Example static value, replace with actual data query
    trees_planted = 5000   # Example static value, replace with actual data query
    renewable_energy_mwh = 1500   # Example static value, replace with actual data query

    context = {
        'total_co2_reduction': total_co2_reduction,
        'trees_planted': trees_planted,
        'renewable_energy_mwh': renewable_energy_mwh
    }
    return render(request, 'impact.html', context)

def register(request):
    # Check if the user is already logged in
    if request.user.is_authenticated:
        messages.info(request, "You are already registered and logged in.")
        return redirect('dashboard')   # Redirect them to the dashboard

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

def logout_page(request):
    logout(request)
    return render(request, 'logout_page.html')

def password_reset(request):
    return render(request, 'password_reset.html')

def list_products(request):
    products = Product.objects.all()
    return render(request, 'list_products.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    electric_consumptions = ElectricConsumption.objects.filter(country=product.country).order_by('year')
    years = [ec.year for ec in electric_consumptions]
    data = [ec.consumption for ec in electric_consumptions]

    context = {
        'product': product,
        'years': years,
        'electric_data': data,
    }

    return render(request, 'product_detail.html', context)

def cart_detail(request):
    try:
        cart = Cart.objects.get(user=request.user, active=True)   # Ensure that 'active' flag is checked if applicable
    except Cart.DoesNotExist:
        cart = None   # Optionally create a new cart if one should always exist

    return render(request, 'cart_detail.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Http404("Product does not exist")

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        cart=cart,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')

@login_required
def update_cart(request):
    if request.method == 'POST':
        for item_id, quantity in request.POST.items():
            if item_id.startswith('quantity-'):
                cart_item_id = item_id.split('-')[1]
                quantity = int(quantity)
                try:
                    cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
                    if quantity > 0:
                        cart_item.quantity = quantity
                        cart_item.save()
                    else:
                        cart_item.delete()
                except CartItem.DoesNotExist:
                    continue
        return redirect('cart_detail')

@login_required
def remove_from_cart(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id, cart__user=request.user)
        item.delete()
    except CartItem.DoesNotExist:
        pass   # Optionally add some user feedback here
    return redirect('cart_detail')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)   # Fetch the user's cart
    if request.method == 'POST':
        return redirect('make_payment')
    else:
        return render(request, 'checkout.html', {'cart': cart})

@login_required
def make_payment(request):
    if request.method == 'POST':
        # Collect payment information from the form
        card_name = request.POST.get('cardName')
        card_number = request.POST.get('cardNumber')
        card_expiry = request.POST.get('cardExpiry')
        card_cvv = request.POST.get('cardCVV')

        # Validate payment information format
        if len(card_number) == 16 and card_cvv.isdigit() and len(card_cvv) == 3:
            # Simulate payment success
            cart = Cart.objects.get(user=request.user)
            for item in cart.items.all():
                Purchase.objects.create(
                    user=request.user,
                    product=item.product,
                    quantity=item.quantity,
                    status='Completed'
                )
                item.delete()   # Clear cart items after purchase

            messages.success(request, "Payment successful!")
            return redirect('payment_status')
        else:
            messages.error(request, "Invalid payment details. Please check your input and try again.")
            return redirect('make_payment')
    else:
        return render(request, 'make_payment.html')

@login_required
def payment_status(request):
    # Clear all existing messages
    storage = messages.get_messages(request)
    storage.used = True

    payment_successful = request.session.get('payment_successful', False)

    if 'payment_successful' in request.session:
        del request.session['payment_successful']

    if payment_successful:
        purchases = Purchase.objects.filter(user=request.user, status='Completed').order_by('-purchase_date')[:10]

        context = {
            'payment_successful': True,
            'purchases': purchases
        }
    else:
        context = {
            'payment_successful': False
        }

    return render(request, 'payment_status.html', context)

@login_required
def dashboard(request):
    context = {}
    items_per_page = 5

    # Paginator for purchases
    purchase_list = Purchase.objects.filter(user=request.user).select_related('product').order_by('-purchase_date')
    purchase_paginator = Paginator(purchase_list, items_per_page)
    page_number = request.GET.get('page', 1)
    purchase_page_obj = purchase_paginator.get_page(page_number)
    purchase_start_index = (purchase_page_obj.number - 1) * items_per_page + 1
    context['purchase_page_obj'] = purchase_page_obj
    context['purchase_start_index'] = purchase_start_index

    if request.user.is_superuser:
        # Calculate total sales and products sold
        total_sales = Purchase.objects.aggregate(
            total_revenue=Sum(F('product__price') * F('quantity'), output_field=DecimalField())
        )['total_revenue'] or Decimal('0.00')
        products_sold = Purchase.objects.aggregate(
            total_sold=Sum('quantity')
        )['total_sold'] or 0

        # Paginator for users
        user_list = User.objects.filter(is_active=True).order_by('username')
        user_paginator = Paginator(user_list, items_per_page)
        user_page_number = request.GET.get('user_page', 1)
        user_page_obj = user_paginator.get_page(user_page_number)
        user_start_index = (user_page_obj.number - 1) * items_per_page + 1

        context.update({
            'total_sales': total_sales,
            'products_sold': products_sold,
            'user_page_obj': user_page_obj,
            'user_start_index': user_start_index,
            'user_total_count': User.objects.filter(is_active=True).count(),
            'is_admin': True
        })
    else:
        context['is_admin'] = False

    return render(request, 'dashboard.html', context)

@login_required
def product_list(request):
    items_per_page = 10
    all_products = Product.objects.all()
    paginator = Paginator(all_products, items_per_page)

    page_number = request.GET.get('page', 1)
    try:
        products_page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        products_page_obj = paginator.get_page(1)
    except EmptyPage:
        products_page_obj = paginator.get_page(paginator.num_pages)

    # Calculate the start index for the current page
    product_start_index = (products_page_obj.number - 1) * items_per_page + 1

    context = {
        'products_page_obj': products_page_obj,
        'product_start_index': product_start_index
    }

    return render(request, 'product_list.html', context)

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('product_list')
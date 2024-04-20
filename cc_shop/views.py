from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, ProfileForm  # Assume these forms are defined
from .models import Cart, CartItem, ElectricConsumption, Product, Purchase, User
from django.db.models import Sum, Count, F
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from datetime import datetime
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

def home(request):
    return render(request, 'home.html')

def logout_page(request):
    logout(request)  # Make sure to actually log the user out
    return render(request, 'logout_page.html')

def about(request):
    """Render the about page."""
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Make sure the import and function call are correct
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})  # Updated path here

def password_reset(request):
    # Implementation would go here, typically sending an email
    return render(request, 'password_reset.html')

def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

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
                item.delete()  # Clear cart items after purchase

            messages.success(request, "Payment successful!")
            return redirect('payment_status')
        else:
            messages.error(request, "Invalid payment details. Please check your input and try again.")
            return redirect('make_payment')
    else:
        return render(request, 'make_payment.html')
    
def payment_status(request):
    # Retrieve payment result from session
    payment_successful = request.session.get('payment_successful', False)  # Defaults to False if not found

    if payment_successful:
        # Get the purchase details
        purchases = Purchase.objects.filter(user=request.user, status='Completed')

        context = {
            'payment_successful': payment_successful,
            'purchases': purchases
        }
    else:
        context = {
            'payment_successful': payment_successful
        }

    return render(request, 'payment_status.html', context)
    
def impact(request):
    # Example data fetching and aggregation
    total_co2_reduction = 10000  # Example static value, replace with actual data query
    trees_planted = 5000  # Example static value, replace with actual data query
    renewable_energy_mwh = 1500  # Example static value, replace with actual data query
    
    context = {
        'total_co2_reduction': total_co2_reduction,
        'trees_planted': trees_planted,
        'renewable_energy_mwh': renewable_energy_mwh
    }
    return render(request, 'impact.html', context)

@login_required
def purchase_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'purchase_product.html', {'product': product})

@login_required
def complete_purchase(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        # Implement your logic for creating a purchase record
        Purchase.objects.create(
            user=request.user,
            product=product,
            price=product.price,
            quantity=1,  # Or modify as needed based on form input
            status='Completed'  # Or start with a different status as per your logic
        )
        # Redirect to a new URL: maybe a thank-you page or order details page
        return redirect('purchase_confirmation')  # Ensure this URL is defined in your urls.py
    else:
        return redirect('purchase_product', product_id=product.id)

@login_required  # Ensure that only logged-in users can add to the cart
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

def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)  # Get the user's cart
    return render(request, 'cart_detail.html', {'cart': cart})

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
        pass  # Optionally add some user feedback here
    return redirect('cart_detail')

@login_required
def dashboard(request):
    context = {}
    purchase_list = Purchase.objects.select_related('user', 'product').order_by('-purchase_date')
    purchase_paginator = Paginator(purchase_list, 5)  # Show 5 purchases per page

    try:
        purchase_page_number = request.GET.get('page', 1)
        purchase_page_obj = purchase_paginator.get_page(purchase_page_number)
    except (PageNotAnInteger, EmptyPage):
        purchase_page_obj = purchase_paginator.get_page(1)

    context['purchase_page_obj'] = purchase_page_obj

    if request.user.is_superuser:
        # Aggregate data for total revenue and total products sold
        total_sales_data = Purchase.objects.aggregate(
            total_revenue=Sum(F('product__price') * F('quantity'))
        )
        total_sales = total_sales_data.get('total_revenue', 0)  # Default to 0 if None
        products_sold = Purchase.objects.aggregate(total_sold=Sum('quantity'))['total_sold'] or 0
        
        # User data and pagination
        user_list = User.objects.filter(is_active=True).order_by('username')
        user_paginator = Paginator(user_list, 5)  # Adjust the number per page as needed
        user_page_number = request.GET.get('user_page', 1)

        try:
            user_page_obj = user_paginator.get_page(user_page_number)
        except (PageNotAnInteger, EmptyPage):
            user_page_obj = user_paginator.get_page(1)
        
        context.update({
            'total_sales': total_sales,
            'products_sold': products_sold,
            'user_page_obj': user_page_obj,
            'user_total_count': user_list.count(),  # Total count of active users
            'is_admin': True
        })
    else:
        context['is_admin'] = False

    return render(request, 'dashboard.html', context)

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)  # Fetch the user's cart
    if request.method == 'POST':
        # Here you would handle the payment processing and finalizing the cart
        # After processing, you can redirect to a confirmation page
        return redirect('make_payment')
    else:
        return render(request, 'checkout.html', {'cart': cart})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    messages.success(request, 'User successfully deleted.')
    return redirect('dashboard')
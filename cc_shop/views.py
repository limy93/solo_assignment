from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, ProfileForm  # Assume these forms are defined
from .models import Cart, CartItem, ElectricConsumption, Product, Purchase, User
from django.db.models import Sum, Count, F
from django.utils import timezone
from django.http import Http404

# Create your views here.

def home(request):
    return render(request, 'home.html')

def logout_page(request):
    return render(request, 'logout_page.html')

def about(request):
    """Render the about page."""
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

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

def product_detail(request, product_code):
    product = get_object_or_404(Product, code=product_code)
    return render(request, 'product_detail.html', {'product': product})

def purchase_confirmation(request):
    # Details of what happens after a purchase would be implemented here
    return render(request, 'purchase_confirmation.html')

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
def dashboard(request):
    # Calculate total sales by summing up the product of price and quantity for all purchases
    total_sales = Purchase.objects.aggregate(total_revenue=Sum(F('product__price') * F('quantity')))

    # Count the total number of products sold
    products_sold = Purchase.objects.aggregate(total_sold=Sum('quantity'))

    # Count active users (example: users who have logged in within the last 30 days)
    active_users = User.objects.filter(last_login__gte=timezone.now() - timezone.timedelta(days=30)).count()

    # Get recent purchases
    recent_purchases = Purchase.objects.select_related('user', 'product').order_by('-purchase_date')[:10]

    context = {
        'total_sales': total_sales['total_revenue'],
        'products_sold': products_sold['total_sold'],
        'active_users': active_users,
        'recent_purchases': recent_purchases,
    }

    return render(request, 'dashboard.html', context)
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, ProfileForm  # Assume these forms are defined
from .models import Cart, CartItem, ElectricConsumption, Product, Purchase

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    """Render the about page."""
    return render(request, 'about.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
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

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    electric_consumptions = ElectricConsumption.objects.filter(country=product.country).order_by('year')
    years = [ec.year for ec in electric_consumptions]
    data = [ec.consumption for ec in electric_consumptions]
    
    return render(request, 'product_detail.html', {
        'product': product,
        'electric_data': data,
        'years': years
    })

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
    
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)  # Ensure the user has a cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1  # Increment the quantity if the item is already in the cart
    cart_item.save()
    return redirect('cart_detail')  # Redirect to a view that shows the cart

def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)  # Get the user's cart
    return render(request, 'cart_detail.html', {'cart': cart})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, ProfileForm  # Assume these forms are defined
from .models import Product

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
    product = Product.objects.get(id=product_id)
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
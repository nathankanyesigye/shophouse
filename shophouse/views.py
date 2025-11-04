from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import BusinessRegistration, Productform
from . models import *
from django.db.models import Q
# Create your views here.
def categories_summary(request):
    return render(request,'categories_summary.html',{})

@login_required
def registerbusiness(request):
    if request.method == 'POST':
        form = BusinessRegistration(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.verification_status = 'pending'
            business.save()
            messages.success(request, "Your business registration has been submitted for review. Our admin team will verify your details.")
            return redirect('home')
    else:
        # Check if user already has a business
        existing_business = RegisterBusiness.objects.filter(owner=request.user).first()
        if existing_business:
            messages.info(request, f"You already have a registered business: {existing_business.name_of_business} ({existing_business.get_verification_status_display()})")
            return redirect('home')
        form = BusinessRegistration()
    return render(request, 'registerbusiness.html', {'form': form})
def product(request, pk):
    product= Product.objects.get(id = pk)
    return render (request , 'product.html' , {'product':product})

#  home page function 
def home(request):
    products = Product.objects.all()
    # Filter out products without images
    products_with_images = [p for p in products if p.image]
    return render(request, 'index.html', { "products": products_with_images })

# register/ signup function
def register(request):
    if request.method  == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
    
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already Used")
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Already exists")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
        
        else:
            messages.info(request, "Invalid Password")
            return redirect('register')
    
    else:
        return render(request, 'register.html')

# Login function
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect ('login')
    else:
        return render (request, "login.html")
    
from django.contrib.auth import logout
from django.shortcuts import redirect

# log out function
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return redirect('home')
    
def update_user(request):
    return render (request, 'update_user.html', {})
    
    
def contact(request):
    return render (request, 'contact.html')
    
    
def about(request):
    return render (request, 'about.html')

# Search products function
   
def search_products(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched= Product.objects.filter(
            Q(name__icontains= searched) | 
            Q(price__icontains= searched) 
            )

        if not searched:
            messages.success(request,"That Product does not exist...Please try again")
            return render(request, 'search.html', {})
        else:

           return render(request,"search.html",{'searched':searched})

    else:
        return render(request, 'search.html', {})
    
# Add product function 
@login_required
def addproduct(request):
    try:
        business = RegisterBusiness.objects.get(owner=request.user)
        
        # Verify business approval status
        if business.verification_status != 'approved':
            messages.warning(request, 
                f"Your business '{business.name_of_business}' needs to be approved before adding products. "
                f"Current status: {business.get_verification_status_display()}")
            return redirect('home')
        
        if request.method == 'POST':
            form = Productform(request.POST, request.FILES)
            if form.is_valid():
                try:
                    product = form.save(commit=False)
                    product.business = business
                    
                    # Validate sale price if product is on sale
                    if product.is_sale and product.sale_price >= product.price:
                        messages.error(request, "Sale price must be less than the regular price.")
                    else:
                        product.save()
                        messages.success(request, 
                            f"Product '{product.name}' has been added successfully to {business.name_of_business}.")
                        return redirect('home')
                except Exception as e:
                    messages.error(request, f"Error saving product: {str(e)}")
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            form = Productform()
        
        context = {
            'form': form,
            'business': business,
            'business_name': business.name_of_business,
            'verification_status': business.get_verification_status_display()
        }
        return render(request, 'addproduct.html', context)
            
    except RegisterBusiness.DoesNotExist:
        messages.error(request, "Please register your business before adding products.")
        return redirect('registerbusiness')


# Update product function
@login_required
def updateproduct(request, pk):
    try:
        product = get_object_or_404(Product, id=pk)
        
        # Check if user owns the business that owns this product
        if not product.business or product.business.owner != request.user:
            messages.error(request, "You don't have permission to edit this product.")
            return redirect('product', pk=pk)
        
        # Check if business is still approved
        if product.business.verification_status != 'approved':
            messages.error(request, 
                f"Your business '{product.business.name_of_business}' is {product.business.get_verification_status_display()}. "
                "You cannot edit products until your business is verified.")
            return redirect('product', pk=pk)
        
        if request.method == 'POST':
            form = Productform(request.POST, request.FILES, instance=product)
            if form.is_valid():
                try:
                    updated_product = form.save(commit=False)
                    # Ensure business association doesn't change
                    updated_product.business = product.business
                    
                    # Validate sale price if product is on sale
                    if updated_product.is_sale and updated_product.sale_price >= updated_product.price:
                        messages.error(request, "Sale price must be less than the regular price.")
                    else:
                        updated_product.save()
                        messages.success(request, f"Product '{updated_product.name}' has been updated successfully.")
                        return redirect('product', pk=pk)
                except Exception as e:
                    messages.error(request, f"Error updating product: {str(e)}")
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            form = Productform(instance=product)
        
        context = {
            'form': form,
            'product': product,
            'business_name': product.business.name_of_business
        }
        return render(request, 'updateproduct.html', context)
        
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')

# delete product function
@login_required
def deleteproduct(request, pk):
    product = get_object_or_404(Product, id=pk)
    if product.business and product.business.owner == request.user:
        product.delete()
    return redirect('home')


#cart functions
from cart.cart import Cart

def cart(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    total = cart.get_total_price()
    context = {
        'cart_products': cart_products,
        'total': total,
    }
    return render(request, 'cart.html', context)

# session function
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# Add cart function
def add_cart(request, product_id):
    cart = Cart(request)
    try:
        product = Product.objects.get(id=product_id)
        cart.add(product)
        return redirect('cart')
    except Product.DoesNotExist:
        return redirect('/')

#Remove cart function  
def remove_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart')
    

# business
def business(request):
    businesses = RegisterBusiness.objects.all()
    return render(request, 'business.html',{'businesses':businesses})
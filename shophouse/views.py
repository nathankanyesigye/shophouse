from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .forms import BusinessRegistration, Productform
from . models import *
from django.db.models import Q
# Create your views here.
def categories_summary(request):
    return render(request,'categories_summary.html',{})

def registerbusiness(request):
    if request.method == 'POST':
        form= BusinessRegistration(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render (request, 'index.html')
    else:
        form = BusinessRegistration()
        return render(request, 'registerbusiness.html',{'form':form})
def product(request, pk):
    product= Product.objects.get(id = pk)
    return render (request , 'product.html' , {'product':product})

#  home page function 
def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', { "products": products })

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
 
def addproduct(request):
    form = Productform()
    if request.method == 'POST':
        form= Productform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    else:
        form = Productform()
        
    context = {
        'form':form
        
    }
    return render(request, 'addproduct.html', context)


# Update product function

def updateproduct(request,pk):
    product = Product.objects.get(id=pk)
    form = Productform(instance=product)
    
    if request.method == 'POST':
        form = Productform(request.POST, request.FILES,  instance=product)
        if form.is_valid():
            form.save()
            return redirect('/')
        
    context = {
        'form':form
        
    }
    return render(request, 'updateproduct.html', context)

# delete product function

def deleteproduct(request,pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('/')


#cart functions

def cart(request,total=0,quantity=0,cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items =CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price* cart_item.quantity)
            quantity+=cart_item.quantity
            
    except Product.DoesNotExist:
        pass
    
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
    }
    return render(request, 'cart.html', context )

# session function
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# Add cart function
def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()
    
    
    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()
    return redirect('/')

#Remove cart function  
def remove_cart(request,product_id):
    cart = Cart.objects.get(cart_id= product_id)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('/')
    

# business
def business(request):
    businesses = RegisterBusiness.objects.all()
    return render(request, 'business.html',{'businesses':businesses})
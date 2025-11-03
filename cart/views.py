from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from shophouse.models import Product
from django.http import JsonResponse

def cart_summary(request):
    cart = Cart(request)
    cart_products =cart.get_prods

    return render(request, 'cart_summary.html', {'cart_products':cart_products})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productId'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product)
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        return response
    elif request.method == 'GET':
        product_id = request.GET.get('id')
        if product_id:
            product = get_object_or_404(Product, id=product_id)
            cart.add(product=product)
        return redirect('cart:cart_summary')

def cart_delete(request, id):
    product = get_object_or_404(Product, id=id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('cart:cart_summary')

def cart_update(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.update(product, quantity)
        return redirect('cart:cart_summary')
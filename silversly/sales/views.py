from models import *
from forms import *
from inventory.models import Product

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core import serializers
from django.http import HttpResponse
from urllib import unquote

def new_receipt(request):
    receipt = None
    try:
        cart = Cart.objects.get(current = True)
    except:
        cart = Cart()
    try:
        receipt = cart.receipt
    except:
        year = datetime.date.today().year - 2000
        index = Receipt.objects.filter(year=year).count()
        receipt = Receipt(year = year, number = index, cart = cart)
        receipt.save()
    
    return redirect(edit_receipt, receipt.id)
    
def edit_receipt(request, id):
    receipt = get_object_or_404(Receipt, pk=id)
    cart = receipt.cart
    customer = receipt.customer
    return render_to_response('cart/edit_receipt.html',  {'products': cart.cartitem_set.all(), 'cart': cart, 'customer': customer, 'receipt': receipt})
        
def save_receipt(request, id):
    receipt = get_object_or_404(Receipt, pk=id)
    cart = receipt.cart
    cart.current = False
    for item in cart.cartitem_set.all():
        if item.update:
            item.product.quantity -= item.quantity
            item.product.save()
    cart.save()
    return redirect(show_receipt, id)

def show_receipt(request, id):
    receipt = get_object_or_404(Receipt, pk=id)
    cart = receipt.cart
    if cart.current:
        redirect(edit_receipt, id)
    customer = receipt.customer
    return render_to_response('sales/show_receipt.html',  {'cart': cart, 'customer': customer, 'receipt': receipt})
    
    
def add_product_to_cart(request):
    bad_request = False
    try:
        cart = Cart.objects.get(current=True)
    except:
        cart = Cart()
        cart.save()
    try:
        product = Product.objects.get(pk=request.GET["product_pk"])
    except:
        product = Product.objects.get(pk=request.POST["product_pk"])
    
    try:	
        cart_item = CartItem.objects.get(product=product, cart=cart)
    except:
        cart_item = CartItem(product=product, cart=cart)
        
    if request.method == "POST":
        form = SellProductForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()                               
            return render_to_response('cart/product_row.html',  {'cart': cart, 'item':  cart_item})
        else:
            bad_request = True	
    else:
        form = SellProductForm(instance=cart_item)
    response = render_to_response('cart/dialogs/add_product.html',  {'form': form, 'cart': cart, 'item': cart_item})
    if bad_request: 
        response.status_code = 400
    return response

def remove_product_from_cart(request, item_id):
    try:
        item = CartItem.objects.get(pk = item_id)
        cart = item.cart
        item.delete()
        return redirect(edit_receipt, cart.id)
    except:
        return HttpResponse(status=400)

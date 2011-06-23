from models import *
from forms import *
from inventory.models import Product
from people.models import *
from django.core.urlresolvers import reverse
from django.db.models import Max
import datetime

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core import serializers
from django.http import HttpResponse
from urllib import unquote
from django.utils import simplejson
from decimal import Decimal


def edit_cart(request):
    try:
        cart = get_object_or_404(Cart, current=True)
    except:
        cart = Cart()
        cart.update_value()
        # is this ok?
        cart.save()

    customer = cart.customer and cart.customer.child()
    return render_to_response('cart/edit_cart.html',  {'products': cart.cartitem_set.all(), 'cart': cart, 'customer': customer})

def edit_cart_customer(request):
    try:
        customer = Customer.objects.get(pk=request.POST["customer_id"])
    except:
        customer = None
    cart = get_object_or_404(Cart, current=True)
    items = cart.cartitem_set.all()
    old_customer = cart.customer
    cart.customer = customer
    #if customer and not (old_customer and customer.pk == old_customer.pk):
    if customer:
        if cart.pricelist != customer.pricelist:
            cart.pricelist = customer.pricelist
            cart.save()
            for item in items:
                item.save()
        if cart.discount != customer.discount:
            cart.discount = customer.discount
    cart.update_value()
    cart.save()
    return render_to_response('cart/product_list.html',  {'products': items, 'cart': cart, 'customer': cart.customer and cart.customer.child()})

def edit_cart_discount(request):
    cart = get_object_or_404(Cart, current=True)
    form = EditDiscountForm(request.POST, instance=cart)
    if form.is_valid():
        cart.update_value()
        form.save()
        return render_to_response('cart/summary.html', {'cart': cart, 'customer': cart.customer and cart.customer.child()})
    else:
        return HttpResponse(status=400)

def edit_cart_pricelist(request):
    cart = get_object_or_404(Cart, current=True)
    form = EditPricelistForm(request.POST, instance=cart)
    if form.is_valid():
        form.save()
        items = cart.cartitem_set.all()
        for item in items:
            item.save()
        cart.update_value()
        cart.save()
        return render_to_response('cart/product_list.html',  {'products': items, 'cart': cart, 'customer': cart.customer and cart.customer.child()})
    else:
        return HttpResponse(status=400)

def get_cart_summary(request):
    cart = get_object_or_404(Cart, current=True)
    return render_to_response('cart/summary.html', {'cart': cart, 'customer': cart.customer and cart.customer.child()})

def toggle_cart_rounding(request):
    cart = get_object_or_404(Cart, current=True)
    cart.rounded = not cart.rounded
    if cart.rounded:
        cart.apply_rounding()
    else:
        cart.update_value()
    cart.save()
    return render_to_response('cart/summary.html', {'cart': cart, 'customer': cart.customer and cart.customer.child()})

def reload_cart(request):
    cart = get_object_or_404(Cart, current=True)
    cart.update_value(deep=True)
    cart.save()
    return redirect(edit_cart)

def new_receipt(request):
    bad_request = False
    cart = get_object_or_404(Cart, current = True)
    scontrino = Scontrino(cart = cart, cf = (cart.customer and cart.customer.cf or ""))

    if request.method == "POST":
        form = ReceiptForm(request.POST, instance=scontrino)
        if form.is_valid():
            form.save()
            cart.current = False
            cart.save()
            for item in cart.cartitem_set.all():
                if item.update:
                    product = item.product
                    product.quantity -= item.quantity
                    product.save()
                    product.sync_to_others("quantity")
            scontrino.send_to_register(close=False)
            return HttpResponse(reverse("show_receipt", args=(scontrino.id,)), mimetype="text/plain")
        else:
            bad_request = True
    else:
        scontrino.payed = cart.discounted_total()
        form = ReceiptForm(instance=scontrino)

    response = render_to_response('cart/dialogs/new_receipt.html',  {'form': form, 'cart': cart, 'receipt': scontrino})
    if bad_request:
        response.status_code = 400
    return response

def show_receipt(request, id):
    receipt = get_object_or_404(Scontrino, pk=id)
    cart = receipt.cart
    customer = cart.customer and cart.customer.child()
    return render_to_response('documents/show_receipt.html',  {'cart': cart, 'customer': customer, 'receipt': receipt})

def pay_due_receipt(request, id):
    receipt = get_object_or_404(Scontrino, pk=id)
    if receipt.due:
        receipt.finally_paid()
    return HttpResponse(status = 200)

def new_invoice(request, customer_id):
    pass

def new_ddt(request):
    bad_request = False
    cart = get_object_or_404(Cart, current = True)
    customer = cart.customer.child()
    now = datetime.datetime.now()
    year = now.year - 2000
    last_ddt_number = Ddt.objects.filter(year = year).aggregate(Max('number'))['number__max']
    number = last_ddt_number and last_ddt_number + 1 or 1
    ddt = Ddt(cart = cart,
        number = number,
        main_address = customer.main_address,
        shipping_address = customer.shipping_address or customer.main_address,
        shipping_date = now)

    if request.method == "POST":
        form = DdtForm(request.POST, instance=ddt)
        if form.is_valid():
            form.save()
            cart.current = False
            cart.save()
            for item in cart.cartitem_set.all():
                if item.update:
                    product = item.product
                    product.quantity -= item.quantity
                    product.save()
                    product.sync_to_others("quantity")
            return HttpResponse(reverse("show_ddt", args=(ddt.id,)), mimetype="text/plain")
        else:
            bad_request = True
    else:
        form = DdtForm(instance=ddt)

    response = render_to_response('cart/dialogs/new_ddt.html',  {'form': form, 'cart': cart})
    if bad_request:
        response.status_code = 400
    return response

def show_ddt(request, id):
    ddt = get_object_or_404(Ddt, pk=id)
    cart = ddt.cart
    customer = cart.customer.child()
    return render_to_response('documents/show_ddt.html',  {'cart': cart, 'customer': customer, 'ddt': ddt})

def print_ddt(request, id):
    from common.views import write_pdf
    ddt = get_object_or_404(Ddt, pk=id)
    cart = ddt.cart
    customer = cart.customer.child()
    shop = Shop.objects.get(site = Site.objects.get_current())
    return write_pdf('pdf/ddt_a5.html',{
        'pagesize' : 'A5',
        'shop': shop,
        'cart' : cart,
        'ddt': ddt})

def add_product_to_cart(request):
    bad_request = False
    try:
        cart = Cart.objects.get(current=True)
    except:
        cart = Cart()
        cart.update_value()
        cart.save()
    try:
        product = Product.objects.get(pk=request.GET["product_pk"])
    except:
        product = Product.objects.get(pk=request.POST["product_pk"])

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
    except:
        cart_item = CartItem(product=product, cart=cart)
        #cart_item.update_value()

    if request.method == "POST":
        form = SellProductForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            cart.update_value()
            cart.save()
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
        cart.update_value()
        cart.save()
        return redirect(edit_cart)
    except:
        return HttpResponse(status=400)

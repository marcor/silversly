from models import *
from forms import *
from inventory.models import Product
from people.models import *
from django.core.urlresolvers import reverse
from django.db.models import Max
import datetime
from copy import deepcopy
from django.conf import settings

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core import serializers
from django.http import HttpResponse
from urllib import unquote
from django.utils import simplejson
from decimal import Decimal
from common.models import *
from common.views import homepage


def edit_cart(request, cart_id=None):
    if cart_id:
        cart = get_object_or_404(Cart, pk=cart_id)
    else:               
        try:
            cart = get_object_or_404(Cart, current=True)
        except:
            cart = Cart()
            cart.update_value()
            # is this ok?
            cart.save()
    customer = cart.customer and cart.customer.child()
    return render_to_response('cart/edit_cart.html',  {'products': cart.cartitem_set.all(), 'cart': cart, 'customer': customer})

def edit_cart_customer(request, cart_id):
    try:
        customer = Customer.objects.get(pk=request.POST["customer_id"])
    except:
        customer = None
    cart = get_object_or_404(Cart, pk=cart_id)
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
        if customer.child().company:
            cart.rounded = False
    cart.update_value()
    cart.save()
    return render_to_response('cart/product_list.html',  {'products': items, 'cart': cart, 'customer': cart.customer and cart.customer.child()})

def edit_cart_discount(request, cart_id):
    cart = get_object_or_404(Cart, pk=cart_id)
    form = EditDiscountForm(request.POST, instance=cart)
    if form.is_valid():
        cart.update_value()
        form.save()
        return render_to_response('cart/summary.html', {'cart': cart, 'customer': cart.customer and cart.customer.child()})
    else:
        return HttpResponse(status=400)

def edit_cart_pricelist(request, cart_id):
    cart = get_object_or_404(Cart, pk=cart_id)
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

def get_cart_summary(request, cart_id=None, json=False):
    if cart_id:
        cart = get_object_or_404(Cart, pk=cart_id)
    else:
        cart = get_object_or_404(Cart, current=True)
    if json:
        json_serializer = serializers.get_serializer("json")()
        data = json_serializer.serialize((cart,), fields = ("final_total", "final_discount"))
        data = '[{"number_of_items": %d, ' % cart.cartitem_set.count() + data[2:]
        return HttpResponse(data, 'application/javascript')
    return render_to_response('cart/summary.html', {'cart': cart, 'customer': cart.customer and cart.customer.child()})

def toggle_cart_rounding(request, cart_id):
    cart = get_object_or_404(Cart, pk=cart_id)
    cart.rounded = not cart.rounded
    if cart.rounded:
        cart.apply_rounding()
    else:
        cart.update_value()
    cart.save()
    return render_to_response('cart/summary.html', {'cart': cart, 'customer': cart.customer and cart.customer.child()})

def reload_cart(request, cart_id):
    cart = get_object_or_404(Cart, pk=cart_id)
    cart.update_value(deep=True)
    cart.save()
    return redirect(edit_cart, cart_id)

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
                item.update_inventory()
            close = Settings.objects.get(site = Site.objects.get_current()).close_receipts
            scontrino.send_to_register(close=close)
            #return HttpResponse(reverse("show_receipt", args=(scontrino.id,)), mimetype="text/plain")
            return HttpResponse(reverse("find_product"), mimetype="text/plain")
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

def new_invoice_from_cart(request, cart_id):
    bad_request = False
    cart = get_object_or_404(Cart, current = True)
    customer = cart.customer.child()
    now = datetime.datetime.now()
    year = now.year - 2000
    try:
        last_invoice = Invoice.objects.order_by('pk')[0]
        number = (last_invoice.year == year) and last_invoice.number + 1 or 1
    except:
        last_invoice = None
        number = 1
    invoice = Invoice(number = number, immediate=True, payment_method=customer.payment_method)

    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        form.prev_invoice = last_invoice
        if form.is_valid():
            form.save(commit = False)
            cart.current = False
            cart.save()
            for item in cart.cartitem_set.all():
                item.update_inventory()
            invoice.cart = cart
            invoice.total_net = cart.discounted_net_total() + invoice.costs
            if invoice.payment_method == "ok":
                invoice.payed = True
            else:
                customer.due += invoice.apply_vat()[0]
                customer.save()
            invoice.save()
            return HttpResponse(reverse("show_invoice", args=(invoice.id,)), mimetype="text/plain")
        else:
            bad_request = True
    else:
        form = InvoiceForm(instance=invoice)

    response = render_to_response('cart/dialogs/new_invoice.html',  {'form': form, 'cart': cart})
    if bad_request:
        response.status_code = 400
    return response

def new_invoice(request, customer_id):
    customer = Customer.objects.get(pk=customer_id).child()
    #open_ddts = Ddt.objects.filter(cart__customer = customer, invoice__isnull = True)
    #if not open_ddts.exists():
     #   return HttpResponse(status=404)

    bad_request = False
    now = datetime.datetime.now()
    year = now.year - 2000
    try:
        last_invoice = Invoice.objects.order_by('pk')[0]
        number = (last_invoice.year == year) and last_invoice.number + 1 or 1
    except:
        last_invoice = None
        number = 1
    invoice = Invoice(number = number, immediate=False, payment_method=customer.payment_method)
    
    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        form.prev_invoice = last_invoice
        form.open_ddts = Ddt.objects.filter(cart__customer = customer, invoice__isnull = True)
        if form.is_valid():
            form.save()
            for ddt in form.open_ddts:
                invoice.ddt_set.add(ddt)
            invoice.total_net = sum(ddt.cart.discounted_net_total() for ddt in form.open_ddts) + invoice.costs
            if invoice.payment_method == "ok":
                invoice.payed = True
            else:
                customer.due += invoice.apply_vat()[0]
                customer.save()
            invoice.save()
            return HttpResponse(reverse("show_invoice", args=(invoice.id,)), mimetype="text/plain")
        else:
            bad_request = True
    else:
        form = InvoiceForm(instance=invoice)

    response = render_to_response('customers/dialogs/new_invoice.html',  {'form': form, 'customer': customer.child()})
    if bad_request:
        response.status_code = 400
    return response

def show_invoice(request, id):
    invoice = get_object_or_404(Invoice, pk=id)
    cart = invoice.cart
    ddts = invoice.ddt_set.all()
    if cart:
        customer = cart.customer.child()
    else:
        customer = ddts[0].cart.customer.child()
    return render_to_response('documents/show_invoice.html',  {'cart': cart, 'customer': customer, 'ddts': ddts, 'invoice': invoice})

def delete_invoice(request):
    try:
        invoice = Invoice.objects.order_by('pk')[0]
    except:
        return HttpResponse(404)
    if request.is_ajax():
        if request.method == "POST" and request.POST["confirm"]:
            if not invoice.payed:
                invoice.finally_paid()
            invoice.delete()
            return HttpResponse(status=200)
        else:
            return render_to_response("documents/dialogs/delete_invoice.html", {'invoice': invoice})
    else:
        return redirect(homepage)

def pay_due_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if not invoice.payed:
        invoice.finally_paid()
    return HttpResponse(status = 200)


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
                item.update_inventory()
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

def print_ddt(request, id, size="a4"):
    from common.views import write_pdf
    ddt = get_object_or_404(Ddt, pk=id)
    cart = ddt.cart
    customer = cart.customer.child()
    shop = Shop.objects.get(site = Site.objects.get_current())
    return write_pdf('pdf/ddt_%s.html' % size,{
        'pagesize' : size,
        'shop': shop,
        'cart' : cart,
        'ddt': ddt})

def print_invoice(request, id, reference_ddts=True):
    from common.views import write_pdf
    invoice = get_object_or_404(Invoice, pk=id)
    cart = invoice.cart
    ddts = invoice.ddt_set.all().order_by("number")
    customer = cart and cart.customer.child() or ddts[0].cart.customer.child()
    shop = Shop.objects.get(site = Site.objects.get_current())
    lines = cart and cart.cartitem_set.count() or 0
    if reference_ddts:
        for ddt in ddts:
            lines = lines + 1 + ddt.cart.cartitem_set.count()
    else:
        for ddt in ddts:
            lines += ddt.cart.cartitem_set.count()
        
    return write_pdf('pdf/invoice_a4.html',{
        'pagesize' : 'a4',
        'shop': shop,
        'cart' : cart,
        'ddts': ddts,
        'reference_ddts': reference_ddts,
        'invoice': invoice,
        'customer': customer,
        'lines': lines,
        'tax': settings.TAX})

def add_product_to_cart(request, cart_id=None):
    bad_request = False
    if not cart_id:
        try:
            cart = Cart.objects.get(current = True)
        except:
            cart = Cart()
            cart.update_value()
            cart.save()
    else:
        cart = Cart.objects.get(pk=cart_id)
        
    try:
        product = Product.objects.get(pk=request.GET["product_pk"])
    except:
        product = Product.objects.get(pk=request.POST["product_pk"])

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
    except:
        cart_item = CartItem(product=product, desc=product.name, cart=cart, quantity=0)
        #cart_item.update_value()
    old_cart_item = deepcopy(cart_item)
    
    if request.method == "POST":
        form = SellProductForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            cart.update_value()
            cart.save()
            # if the cart content has already been removed from the inventory...
            if cart.receipt:
                cart_item.correct_inventory(relative_to=old_cart_item)
                # this gives a consistent result for ddts only, as of now
                # todo: call an "amend" method for invoices and cash register receipts?
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
        # if the cart content has already been removed from the inventory...
        if cart.receipt:
            item.restore_inventory()
        item.delete()
        cart.update_value()
        cart.save()
        return redirect(edit_cart, cart.id)
    except:
        return HttpResponse(status=400)

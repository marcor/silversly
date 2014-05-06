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
from inventory.views import find_product

def edit_cart(request, cart_id=None):
    if cart_id:
        cart = get_object_or_404(Cart, pk=cart_id)
    else:               
        try:
            cart = Cart.objects.filter(current=True)[0]
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
        cart = get_object_or_404(Cart, pk=request.GET["cart_pk"])
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

def merge_carts(source, dest):
	for item in source.cartitem_set.all():
		item.cart = dest
		if source.pricelist == dest.pricelist:
			item.save(update_value=False)
		else:
			item.save()
	dest.update_value()
	return dest

def suspend_cart(request, cart_id):
    cart = get_object_or_404(Cart, pk=cart_id)
    suspended_cart = cart.get_suspended()
    if suspended_cart:
        merge_carts(cart, suspended_cart)
        suspended_cart.save() 
        cart.delete()
        return redirect(edit_cart, suspended_cart.id)
    else:
        cart.suspended = True
        cart.current = False
        cart.save()
        return redirect(edit_cart, cart_id)

def resume_cart(request, cart_id):
    cart = get_object_or_404(Cart, pk=cart_id)
    if cart.suspended ==True:
        cart.suspended = False
        cart.current = True
        cart.save()
    return redirect(edit_cart, cart.id)
    
def merge_suspended(request, cart_id):
     cart = get_object_or_404(Cart, pk=cart_id)
     suspended_cart = get_object_or_404(Cart, customer=cart.customer, suspended = True)
     merge_carts(suspended_cart, cart)
     cart.save()
     suspended_cart.delete()
     cart.suspended_cart = None
     return redirect(edit_cart, cart.id) 

def new_receipt(request, cart_id):
    bad_request = False
    cart = get_object_or_404(Cart, current = True, pk=cart_id)
    scontrino = Scontrino(cart = cart, cf = (cart.customer and cart.customer.cf or ""))

    if request.method == "POST":
        form = ReceiptForm(request.POST, instance=scontrino)
        if form.is_valid():
            form.save()
            cart.current = False
            cart.save()
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
    cart = get_object_or_404(Cart, current = True, pk=cart_id)
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
            if invoice.immediate:
                invoice.cart.current = True
                invoice.cart.save()
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


def new_ddt(request, cart_id):
    bad_request = False
    cart = get_object_or_404(Cart, current = True, pk=cart_id)
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

def delete_ddt(request):
    try:
        ddt = Ddt.objects.order_by('pk')[0]
    except:
        return HttpResponse(404)
    if request.is_ajax():
        if request.method == "POST" and request.POST["confirm"]:
            ddt.cart.current = True
            ddt.cart.save()
            ddt.delete()
            return HttpResponse(status=200)
        else:
            return render_to_response("documents/dialogs/delete_ddt.html", {'ddt': ddt})
    else:
        return redirect(homepage)

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
        'lines': lines})

def add_product_to_cart(request, cart_id=None):
    bad_request = False
    new_cart = False
    cart_id = cart_id or request.GET.get("cart_pk", None)
    if not cart_id:
        cart = Cart()
        cart.update_value()
        cart.save()
        new_cart = True
    else:
        cart = Cart.objects.get(pk=cart_id)
    
    product_id = request.GET.get("product_pk", None) or request.POST.get("product_pk", None)
    product = Product.objects.get(pk=product_id)
    try:
        # bug: with suspended carts, multiple items for the same product can exist
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
            cart_item.correct_inventory(relative_to=old_cart_item)
            return render_to_response('cart/product_row.html',  {'cart': cart, 'item':  cart_item})
        else:
            bad_request = True
    else:
        form = SellProductForm(instance=cart_item)
    response = render_to_response('cart/dialogs/add_product.html',  {'form': form, 'cart': cart, 'item': cart_item, 'new_cart': new_cart})
    if bad_request:
        response.status_code = 400
    return response

def remove_product_from_cart(request, item_id):
    try:
        item = CartItem.objects.get(pk = item_id)
        cart = item.cart
    except:
        return HttpResponse(status=400)

    if request.is_ajax():
        if request.method == "POST" and request.POST["confirm"]:
            item.restore_inventory()
            item.delete()
            open_carts = Cart.objects.filter(current = True)
            if (cart.suspended or open_carts.count() > 1) and cart.is_empty():
                cart.delete()
                return HttpResponse(content=reverse('find_product'), content_type="text/plain")
            cart.update_value()
            cart.save()
            return HttpResponse(content=reverse('revise_cart', args=(cart.id,)), content_type="text/plain")
        else:
            return render_to_response("cart/dialogs/delete_product.html", {'item': item})
    else:
        return redirect(edit_cart, cart.id)
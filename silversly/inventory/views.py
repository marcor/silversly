from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from models import *
from forms import *
from django.forms.models import inlineformset_factory
from django.db.models import Q
from django.core import serializers
from django.http import HttpResponse
from urllib import unquote
from django.utils import simplejson

#
# ARTICOLI
#

def find_product(request):
    # just shows a minimalistic search form (by name and code)
    return render_to_response('product/find.html')

def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    return render_to_response('product/show.html', {'product': product})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = form.save()
            
            if request.is_ajax():
                return HttpResponse(status=200)
            else:
                return redirect(show_product, new_product.id)
    else:
        form = ProductForm()
    return render_to_response('product/%sadd.html' % (request.is_ajax() and 'ajax_' or ''), {'form': form})

def load_products(request):
    pass
    
def list_by_category(request, id):
    category = get_object_or_404(Category, pk=id)
    child_categories = Category.objects.filter(parent = category)
    products = Product.objects.filter(category = category)
    return render_to_response('category/list.html', {'category': category, 'children': child_categories, 'products': products})

def list_categories(request):
    categories = Category.objects.filter(parent = None)
    return render_to_response('category/root_list.html', {'children': categories})

def add_category(request, parent_id=None, formclass=None):
    if request.method == "POST":
        form = formclass(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            if parent_id:
                new_category.parent = Category.objects.get(pk=parent_id)
            new_category.save()
            if request.is_ajax():
                return HttpResponse(status=200)
            else:
                return redirect(list_by_category, new_category.id)
    else:
        form = formclass()
    if request.is_ajax():
        template = 'category/dialogs/add.html'
    else:
        template = 'category/add.html'
    return render_to_response(template, {'form': form})


#
#   FORNITORI
#

def find_supplier(request):
    if request.is_ajax():
        term = unquote(request.GET["term"])
        matching_suppliers = Supplier.objects.filter(name__icontains = term)
        data = serializers.serialize("json", matching_suppliers)
        return HttpResponse(data, 'application/javascript')
    return render_to_response('suppliers/find.html')
    
def show_supplier(request, id):
    supplier = get_object_or_404(Supplier, pk=id)
    return render_to_response('suppliers/show.html', {'supplier': supplier})

def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            new_supplier = form.save()
            if request.is_ajax():
                return render_to_response('suppliers/ajax_add.html')
            else:
                return redirect(show_supplier, new_supplier.id)
    else:
        form = SupplierForm()
    return render_to_response('suppliers/%sadd.html' % (request.is_ajax() and 'ajax_' or ''), {'form': form})

#
#   CLIENTI
#

def find_customer(request):
    return render_to_response('customers/find.html')
    
def show_customer(request, id):
    customer = get_object_or_404(Customer, pk=id)
    return render_to_response('customers/show.html', {'customer': customer})

def add_customer(request):
    #CustomerFormset = inlineformset_factory(Address, Customer, fk_name="main_address")
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            new_customer = form.save()
            return redirect(show_customer, new_customer.id)
    else:
        form = CustomerForm()
        print form
    return render_to_response('customers/%sadd.html' % (request.is_ajax() and 'ajax_' or ''), {'form': form})

#
# VENDITE
#

def show_cart(request):
    pass

#____________________
#
# AJAX only views 
#____________________
#

#---- children of the show_product view

def product_tab(request, id):
    product = get_object_or_404(Product, pk=id)
    bad_request = False
    if request.method == "POST":
        form = ProductForm(request.POST, instance = product)
        if form.is_valid():
            form.save()
        else:
            bad_request = True
    else:
        form = ProductForm(instance = product)
    response = render_to_response('product/tabs/main.html', {'form': form, 'product': product})
    if bad_request: 
        response.status_code = 400
    return response

def prices_tab(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render_to_response('product/tabs/prices.html', {'product': product, 
            'can_add_supply': product.suppliers.count() < Supplier.objects.count()})

def list_supplies(request, product_id, simple=False):
    supplies = Supply.objects.filter(product__id = product_id)
    if simple:
        return render_to_response('supply/list_simple.html', {'supplies': supplies})
    else:
        return render_to_response('supply/list.html', {'supplies': supplies, 'product': Product.objects.get(pk=product_id)})
    
def add_supply(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    bad_request = False
    supply = Supply(product = product)
    if request.method == "POST":
        form = SupplyForm(request.POST, instance = supply)
        if form.is_valid():
            form.save()
        else:
            bad_request = True
    else:
        form = SupplyForm(instance = supply)
    # query da semplificare: Supplier.objects.exclude(products__in ... ) o qualcosa del genere
    form.fields["supplier"].queryset = Supplier.objects.exclude(pk__in=product.suppliers.all())
    response = render_to_response('product/dialogs/add_supply.html', {'form':  form, 'product': product})
    if bad_request: 
        response.status_code = 400
    return response

def remove_supply(request, supply_id):
    if request.is_ajax():
        supply = get_object_or_404(Supply, pk=supply_id)
        supply.delete()
        return HttpResponse(status=200)
    return HttpResponse(status=400)

def modify_supply(request, supply_id):
    supply = get_object_or_404(Supply, pk=supply_id)
    bad_request = False
    if request.method == "POST":
        form = ModifySupplyForm(request.POST, instance = supply)
        if form.is_valid():
            form.save()
        else:
            bad_request = True
    else:
        form = ModifySupplyForm(instance = supply)
    #del(form.fields["supplier"])
    response = render_to_response('product/dialogs/modify_supply.html', {'form':  form, 'supply': supply})
    if bad_request: 
        response.status_code = 400
    return response

def list_markups(request, product_id):
    markups = list(Markup.objects.filter(product = product_id))
    product = Product.objects.get(pk=product_id)
    #vanilla_pricelists = Pricelist.objects.exclude(name__in = [markup.pricelist.name for markup in markups])
        
    pricelists = Pricelist.objects.all()
    for pricelist in pricelists:
        for markup in markups:
            if markup.pricelist == pricelist:
                pricelist.markup = markup
                markups.remove(markup)
                pricelist.customized = True
                break
        else:
            markup = Markup(product=product, pricelist=pricelist, charge=pricelist.default_markup)
            # this does not save anything to the db!
            pricelist.markup = markup
        pricelist.price = pricelist.markup.calculate_price()
        
    return render_to_response('markup/list.html', {'pricelists': pricelists, 'product': product})

def modify_markup(request, product_id, pricelist_id):
    try:
        markup = Markup.objects.get(product__id = product_id, pricelist__name = pricelist_id)
    except Markup.DoesNotExist:
        product = Product.objects.get(pk=product_id)
        pricelist = Pricelist.objects.get(pk=pricelist_id)
        markup = Markup(product = product, pricelist = pricelist)
    bad_request = False
    if request.method == "POST":
        form = ModifyMarkupForm(request.POST, instance = markup)
        if form.is_valid():
            form.save()
        else:
            bad_request = True
    else:
        form = ModifyMarkupForm(instance = markup)
    response = render_to_response('product/dialogs/modify_markup.html', {'form':  form, 'markup': markup})
    if bad_request: 
        response.status_code = 400
    return response   
        
        
def remove_markup(request, markup_id):
    if request.is_ajax():
        markup = get_object_or_404(Markup, pk=markup_id)
        markup.delete()
        return HttpResponse(status=200)
    return HttpResponse(status=400)

        

def history_tab(request, product_id):
    product = get_object_or_404(Product, pk=id)
    return render_to_response('product/tabs/history.html', {'product': product})

#---- children ogf the show_supplier view

def supplier_info_tab(request, id):
    supplier = get_object_or_404(Supplier, pk=id)
    bad_request = False
    if request.method == "POST":
        form = SupplierForm(request.POST, instance = supplier)
        if form.is_valid():
            form.save()
        else:
            bad_request = True
    else:
        form = SupplierForm(instance = supplier)
    response = render_to_response('suppliers/tabs/info.html', {'form': form, 'supplier': supplier})
    if bad_request: 
        response.status_code = 400
    return response

def supplier_history_tab(request, supplier_id):
    supplier = get_object_or_404(Costumer, pk=supplier_id)
    return render_to_response('suppliers/tabs/history.html', {'supplier': supplier})

#---- children ogf the show_customer view

def customer_info_tab(request, id):
    customer = get_object_or_404(Customer, pk=id)
    bad_request = False
    if request.method == "POST":
        form = CustomerForm(request.POST, instance = customer)
        if form.is_valid():
            form.save()
        else:
            bad_request = True
    else:
        form = CustomerForm(instance = customer)
    response = render_to_response('customers/tabs/info.html', {'form': form, 'customer': customer})
    if bad_request: 
        response.status_code = 400
    return response

def customer_history_tab(request, customer_id):
    customer = get_object_or_404(Costumer, pk=customer_id)
    return render_to_response('customers/tabs/history.html', {'customer': customer})

#---- autocomplete for string fields

def ajax_find_product(request):
    if request.is_ajax():
        term = unquote(request.GET["term"])
        matches = Product.objects.filter(Q(name__icontains = term) | Q(code__icontains = term))
        json_serializer = serializers.get_serializer("json")()
        json_serializer.serialize(matches, ensure_ascii=False)
        data = json_serializer.serialize(matches, fields = ("name", "code", "quantity", "min_quantity", "unit", "base_price"))
        if matches.count() == 1:
            data = '[{"perfect_match": true, ' + data[2:]
        return HttpResponse(data, 'application/javascript')
    return HttpResponse(status=400)

#--- sort this

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    bad_request = False
    try:
        cart = Cart.objects.get(current = True)
    except:
        cart = Cart()
        cart.save()
    item = CartItem(product = product, cart = cart)
    
    if request.method == "POST":
        form = CartItemForm(request.POST, instance = item)
        if form.is_valid():
            form.save()
        else:
            bad_request = True
    else:
        form = CartItemForm(instance = item)
    
    response = render_to_response('cart/dialogs/add_product.html', {'form':  form, 'item': item})
    if bad_request: 
        response.status_code = 400
    return response

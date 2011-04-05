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
    status = 200
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = form.save()
            if request.is_ajax():
                return HttpResponse(str(new_product.id), status=200,  mimetype="text/plain")
            return redirect(show_product, new_product.id)
        else:
            status = 400
    else:
        form = ProductForm()
    if request.is_ajax():
        response  = render_to_response('product/ajax_add.html', {'form': form})
        response.status_code = status
        return response
    else:
        return render_to_response('product/add.html', {'form': form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.is_ajax():
        if request.method == "POST" and request.POST["confirm"]:
            product.delete()
            return HttpResponse(status=200)
        else:
            return render_to_response("product/dialogs/delete.html", {'product': product})
    else:
        return redirect(show_product, product_id)

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
# RIFORNIMENTI
#

def new_batch_load(request):
    open_batches = BatchLoad.objects.filter(loaded=False)
    if open_batches.count():
        batch = open_batches[0]
    else:
        batch = BatchLoad()
        batch.save()
    return redirect(show_batch_load, batch.pk)
        

def show_batch_load(request, batch_id):
    if request.method == "GET":
        batch = BatchLoad.objects.get(pk=batch_id)
        supplier_form = BatchSupplierForm(instance=batch)
        products = IncomingProduct.objects.filter(batch=batch)
        return render_to_response('batch_load/show.html',  {'base_form': supplier_form, 'products': products, 'batch': batch})
        
    if request.is_ajax() and request.method == "POST":
        batch = BatchLoad.objects.get(pk=batch_id)
        supplier_form = BatchSupplierForm(request.POST, instance = batch)
        if supplier_form.is_valid():
            supplier_form.save()
            return HttpResponse(status=200)
    return HttpResponse(status=400)
    
    
def save_batch_load(request, batch_id):
    batch = BatchLoad.objects.get(pk=batch_id)
    products = IncomingProduct.objects.filter(batch=batch)
    for item in products:
        dest = item.actual_product
        try:
            supply = Supply.objects.get(supplier = batch.supplier, product = dest)
        except:
            supply = Supply(supplier = batch.supplier, product = dest)
        new_prices = NewPrice.objects.filter(product = item)
        for new_price in new_prices:
            try:
                price = Price.objects.get(pricelist = new_price.pricelist, product = dest)
            except:
                price = Price(pricelist = new_price.pricelist, product = dest)
            price.method = new_price.method
            price.gross = new_price.value
            price.markup = new_price.markup
            price.save()

        dest.quantity += item.quantity
        supply.price = item.new_supplier_price
        supply.code = item.new_supplier_code
        supply.save()
        dest.save()		
    
    batch.loaded = True
    batch.save()
    return redirect(new_batch_load)

def add_product_to_batch(request, batch_id):
    bad_request = False
    batch = BatchLoad.objects.get(pk=batch_id)
    try:
        product = Product.objects.get(pk=request.GET["product_pk"])
    except:
        product = Product.objects.get(pk=request.POST["product_pk"])
    
    try:
        supply = Supply.objects.get(supplier=batch.supplier, product=product)
        newsupplier = False
    except:
        supply = Supply(product=product, supplier=batch.supplier)
        newsupplier = True
    try:	
        editable_product = IncomingProduct.objects.get(actual_product=product, batch=batch)
    except:
        editable_product = IncomingProduct(actual_product=product, batch=batch, 
             new_supplier_code=supply.code,
             new_supplier_price=supply.price)
        
    if request.method == "POST":
        form = IncomingProductForm(request.POST, instance=editable_product)
        if form.is_valid():
            if editable_product.pk:
                form.save()
            else:
                form.save() 
                actual_prices = Price.objects.filter(product = editable_product.actual_product)
                print actual_prices
                for price in actual_prices:
                    newprice = NewPrice(method = price.method, value = price.gross, markup = price.markup, product = editable_product, pricelist = price.pricelist)
                    newprice.save()
                               
            return render_to_response('batch_load/product_row.html',  {'batch': batch, 'item':  editable_product})
        else:
            bad_request = True	
    else:
        form = IncomingProductForm(instance=editable_product)
    response = render_to_response('batch_load/dialogs/add_product.html',  {'form': form, 'batch': batch, 'product':  product, 'newsupplier': newsupplier})
    if bad_request: 
        response.status_code = 400
    return response

def remove_product_from_batch(request, batch_id, iproduct_id):
    try:
        IncomingProduct.objects.get(pk = iproduct_id).delete()
        return redirect(show_batch_load, batch_id)
    except:
        return HttpResponse(status=400)
        
def create_product_dialog(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = form.save()
            return HttpResponse(status=200)
        else:
            status = 400
    else:
        form = ProductForm()
        status = 200
    response = render_to_response('product/dialogs/add.html', {'form': form})
    response.status_code = status
    return response

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

def list_supplies(request, product_id):
    supplies = Supply.objects.filter(product__id = product_id)
    return render_to_response('supply/list.html', {'supplies': supplies, 'product': Product.objects.get(pk=product_id)})
    
def list_supplies_readonly(request, product_id):
    supplies = Supply.objects.filter(product__id = product_id)
    return render_to_response('supply/list_simple.html', {'supplies': supplies})
    
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

def list_prices(request, product_id):
    prices = list(Price.objects.filter(product = product_id))
    product = Product.objects.get(pk=product_id)
    #vanilla_pricelists = Pricelist.objects.exclude(name__in = [markup.pricelist.name for markup in markups])
        
    pricelists = Pricelist.objects.all()
    for pricelist in pricelists:
        for price in prices:
            if price.pricelist == pricelist:
                pricelist.price = price
                prices.remove(price)
                pricelist.customized = True
                break
        else:
            price = Price(product=product, pricelist=pricelist, markup=pricelist.default_markup, method=pricelist.default_method)
            # this does not save anything to the db!
            price.update()
            pricelist.price = price
        if pricelist.price.method == '==':    
            pricelist.desc = "Prezzo fisso"
        elif pricelist.price.method == '%~':
            pricelist.desc = "Prezzo base + %d%% (arrotondato)" % pricelist.price.markup 
        else:
            pricelist.desc = "Prezzo base + %d%%" % pricelist.price.markup
        price.tax = price.gross - price.net
    return render_to_response('markup/list.html', {'pricelists': pricelists, 'product': product})
    
def list_temp_prices(request):
    product_id = request.GET["product_pk"]
    prices = list(NewPrice.objects.filter(product = product_id))
    product = IncomingProduct.objects.get(pk=product_id)
    #vanilla_pricelists = Pricelist.objects.exclude(name__in = [markup.pricelist.name for markup in markups])
        
    pricelists = Pricelist.objects.all()
    for pricelist in pricelists:
        for price in prices:
            if price.pricelist == pricelist:
                pricelist.price = price
                prices.remove(price)
                pricelist.customized = True
                break
        else:
            price = NewPrice(product=product, pricelist=pricelist, markup=pricelist.default_markup, method=pricelist.default_method)
            # this does not save anything to the db!
            pricelist.price = price
        pricelist.calculated_price = pricelist.price.calculate_price()
        if pricelist.price.method == '==':    
            pricelist.desc = "Prezzo fisso"
        elif pricelist.price.method == '%~':
            pricelist.desc = "Prezzo base + %d%% (arrotondato)" % pricelist.price.markup 
        else:
            pricelist.desc = "Prezzo base + %d%%" % pricelist.price.markup 
    return render_to_response('markup/list_temp.html', {'pricelists': pricelists, 'product': product})

def modify_price(request, product_id, pricelist_id):
    try:
        price = Price.objects.get(product__id = product_id, pricelist__name = pricelist_id)
    except Price.DoesNotExist:
        product = Product.objects.get(pk=product_id)
        pricelist = Pricelist.objects.get(pk=pricelist_id)
        price = Price(product = product, pricelist = pricelist, method = pricelist.default_method, markup = pricelist.default_markup, gross = 0)
    bad_request = False
    if request.method == "POST":
        form = ModifyPriceForm(request.POST, instance = price)
        if form.is_valid():
            form.save()
        else:
            bad_request = True
    else:
        form = ModifyPriceForm(instance = price)
    response = render_to_response('product/dialogs/modify_markup.html', {'form':  form, 'price': price})
    if bad_request: 
        response.status_code = 400
    return response   
        
        
def reset_price(request, price_id):
    if request.is_ajax():
        price = get_object_or_404(Price, pk=price_id)
        price.delete()
        return HttpResponse(status=200)
    return HttpResponse(status=400)
    
def modify_temp_price(request, product_id, pricelist_id):
    try:
        price = NewPrice.objects.get(product__id = product_id, pricelist__name = pricelist_id)
    except NewPrice.DoesNotExist:
        product = IncomingProduct.objects.get(pk=product_id)
        pricelist = Pricelist.objects.get(pk=pricelist_id)
        price = NewPrice(product = product, pricelist = pricelist, method = pricelist.default_method, markup = pricelist.default_markup, value=0)
    bad_request = False
    if request.method == "POST":
        form = ModifyPriceForm(request.POST, instance = price)
        if form.is_valid():
            form.save()
        else:
            bad_request = True
    else:
        form = ModifyPriceForm(instance = price)
    response = render_to_response('product/dialogs/modify_markup_temp.html', {'form':  form, 'price': price})
    if bad_request: 
        response.status_code = 400
    return response   
        
        
def reset_temp_price(request, price_id):
    if request.is_ajax():
        price = get_object_or_404(NewPrice, pk=price_id)
        price.delete()
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

def get_name_query(term):
    words = term.split(" ")
    if len(words) > 1:
        words = filter(lambda x: None or x.strip(), words)
    word_query = Q()
    for word in words:
        word_query &= Q(name__istartswith = word) | Q(name__icontains = " " + word)
    return word_query

def get_code_query(term):
    return Q(code__icontains = term)
    
def ajax_find_product(request):
    if request.is_ajax():
        term = unquote(request.GET["term"])
        word_query = get_name_query(term)
        code_query = get_code_query(term)
        
        if "supplier" in request.GET:
            matches = Product.objects.filter(word_query | code_query, suppliers__id = request.GET["supplier"])
        else:
           matches = Product.objects.filter(word_query | code_query)

        #matches = Product.objects.filter(Q(name__istartswith = term) | Q(name__icontains = " " + term) | Q(code__icontains = term))
        json_serializer = serializers.get_serializer("json")()
        json_serializer.serialize(matches, ensure_ascii=False)
        data = json_serializer.serialize(matches, fields = ("name", "code", "quantity", "min_quantity", "unit", "base_price"))
        if matches.count() == 1:
            data = '[{"perfect_match": true, ' + data[2:]
        return HttpResponse(data, 'application/javascript')
    return HttpResponse(status=400)

def ajax_find_product2(request):
    if request.is_ajax():
        
        term = unquote(request.GET["term"])        
        
        word_query = get_name_query(term)
        code_query = get_code_query(term)       
        
        #matches = Product.objects.filter(Q(name__istartswith = term) | Q(name__icontains = " " + term) | Q(code__icontains = term))
        json_serializer = serializers.get_serializer("json")()
        json_serializer.serialize(matches, ensure_ascii=False)
        data = json_serializer.serialize(matches, fields = ("name", "code", "quantity", "min_quantity", "unit", "base_price"))
        if matches.count() == 1:
            data = '[{"perfect_match": true, ' + data[2:]
        return HttpResponse(data, 'application/javascript')
    return HttpResponse(status=400)


def ajax_get_prices(request, product_id, pricelist):
    if request.is_ajax():
        pricelist = Pricelist.objects.get(name=pricelist)
        try:
            price = Price.objects.get(product = product_id, pricelist = pricelist)
        except:
            price = Price(product=Product.objects.get(pk=product_id), pricelist=pricelist, markup=pricelist.default_markup, method=pricelist.default_method)
            price.update()
        data = simplejson.dumps({'net': str(price.net), 'gross': str(price.gross), 'tax': str(price.gross - price.net)})
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

from models import *
from forms import *
#from inventory.models import Product

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core import serializers
from django.http import HttpResponse
from urllib import unquote

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
    
def show_supplier(request, id):
    supplier = get_object_or_404(Supplier, pk=id)
    return render_to_response('suppliers/show.html', {'supplier': supplier})

#---- children of the show_supplier view

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


#
#   CLIENTI
#

def find_customer(request):
    return render_to_response('customers/find.html')

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

def show_customer(request, id):
    customer = get_object_or_404(Customer, pk=id)
    return render_to_response('customers/show.html', {'customer': customer})
    
#---- children of the show_customer view

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
    customer = get_object_or_404(Customer, pk=customer_id)
    return render_to_response('customers/tabs/history.html', {'customer': customer})

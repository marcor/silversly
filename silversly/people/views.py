from models import *
from forms import *
#from inventory.models import Product
from sales.models import *
from common.views import DecimalEncoder

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core import serializers
from django.utils import simplejson
from django.db.models import Q
from django.http import HttpResponse
from urllib import unquote

def get_name_query(term):
    words = term.split(" ")
    if len(words) > 1:
        words = filter(lambda x: None or x.strip(), words)
    word_query = Q()
    for word in words:
        word_query &= Q(name__istartswith = word) | Q(name__icontains = " " + word)
    return word_query

#
#   FORNITORI
#

def find_supplier(request):
    if request.is_ajax():
        term = unquote(request.GET["term"])
        name_query = get_name_query(term)
        matches = Supplier.objects.filter(name_query)
        result_list = []
        for supp in matches:
            result_list.append(supp.to_dict())
        if len(result_list) == 1:
            result_list[0]["perfect_match"] = True
        return HttpResponse(simplejson.dumps(result_list, cls=DecimalEncoder), 'application/javascript')
    else:
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
    if request.is_ajax():
        term = unquote(request.GET["term"])
        name_query = get_name_query(term)
        matches = Customer.objects.filter(name_query)
        result_list = []
        for cust in matches:
            result_list.append(cust.to_dict())
        if len(result_list) == 1:
            result_list[0]["perfect_match"] = True
        return HttpResponse(simplejson.dumps(result_list, cls=DecimalEncoder), 'application/javascript')
    else:
        return render_to_response('customers/find.html')

def add_customer(request):
    status = 200
    if request.is_ajax():
        Form = CustomerQuickForm
    else:
        Form = CustomerForm
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            new_customer = form.save()
            if request.is_ajax():
                return HttpResponse(simplejson.dumps(new_customer.to_dict(), cls=DecimalEncoder), 'application/javascript')
            return redirect(show_customer, new_customer.id)
        else:
            status = 400
    else:
        form = Form()

    if request.is_ajax():
        response  = render_to_response('customers/ajax_add.html', {'form': form})
        response.status_code = status
        return response
    else:
        return render_to_response('customers/add.html', {'form': form})

def add_company(request):
    status = 200
    if request.is_ajax():
        Form = CompanyQuickForm
    else:
        Form = CompanyForm
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            new_company = form.save()
            if request.is_ajax():
                return HttpResponse(simplejson.dumps(new_company.to_dict(), cls=DecimalEncoder), 'application/javascript')
            return redirect(show_customer, new_company.id)
        else:
            status = 400
    else:
        form = Form()

    if request.is_ajax():
        response  = render_to_response('customers/ajax_add_company.html', {'form': form})
        response.status_code = status
        return response
    else:
        return render_to_response('customers/add.html', {'form': form})



def show_customer(request, id):
    customer = get_object_or_404(Customer, pk=id)
    try:
        if customer.companycustomer:
            customer.company = customer.companycustomer
    except:
        pass
    return render_to_response('customers/show.html', {'customer': customer})


#---- children of the show_customer view

def customer_info_tab(request, id):
    customer = get_object_or_404(Customer, pk=id)
    bad_request = False
    try:
        customer = customer.companycustomer
        company = True
    except:
        company = False
    if company:
        Form = CompanyInfoForm
    else:
        Form = CustomerInfoForm

    if request.method == "POST":
        form = Form(request.POST, instance = customer)
        if form.is_valid():
            form.save()
        else:
            bad_request = True
    else:
        form = Form(instance = customer)
    response = render_to_response('customers/tabs/info.html', {'form': form, 'customer': customer})
    if bad_request:
        response.status_code = 400
    return response

def customer_commercial_tab(request, id):
    customer = get_object_or_404(Customer, pk=id)
    bad_request = False
    try:
        customer = customer.companycustomer
        company = True
    except:
        company = False
    if company:
        Form = CompanyCommercialForm
    else:
        Form = CustomerCommercialForm

    if request.method == "POST":
        form = Form(request.POST, instance = customer)
        if form.is_valid():
            form.save()
        else:
            bad_request = True
    else:
        form = Form(instance = customer)
    response = render_to_response('customers/tabs/commercial.html', {'form': form, 'customer': customer})
    if bad_request:
        response.status_code = 400
    return response

def customer_history_tab(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    carts = Cart.objects.filter(customer = customer, receipt__isnull = False)
    receipts = Receipt.objects.filter(cart__in = carts)
    list = []
    for r in receipts:
        list.append(r.child())
    return render_to_response('customers/tabs/history.html', {'customer': customer.child(), 'receipts': list})

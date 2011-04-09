from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect

from inventory.models import *
from people.models import *
from sales.models import *

def homepage(request):
    outstock = Product.objects.raw("select * from inventory_product where quantity < min_quantity order by name collate nocase")
    open_batchloads = BatchLoad.objects.filter(loaded = False)
    last_receipts = Receipt.objects.order_by("-date")[:5]
    last_ddts = Ddt.objects.order_by("-date")[:5]
    debtors = RetailCustomer.objects.raw("select * from people_retailcustomer where due > 0 collate nocase")
    
    return render_to_response("home.html", 
        {'outstock': list(outstock),
        'open_batchloads': open_batchloads,
        'last_receipts': last_receipts,
        'last_ddts': last_ddts,
        'debtors': list(debtors)})


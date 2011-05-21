from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse

import json, decimal

from inventory.models import *
from people.models import *
from sales.models import *
from forms import *


# utility functions

class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)


# actual views

def homepage(request):
    outstock = Product.objects.raw("select * from inventory_product where quantity < min_quantity order by name collate nocase")
    open_batchloads = BatchLoad.objects.filter(loaded = False)
    last_receipts = Receipt.objects.order_by("-date")[:5]
    last_ddts = Ddt.objects.order_by("-date")[:5]
    debtors = Customer.objects.raw("select * from people_customer where due > 0 collate nocase")

    return render_to_response("home.html",
        {'outstock': list(outstock),
        'open_batchloads': open_batchloads,
        'last_receipts': last_receipts,
        'last_ddts': last_ddts,
        'debtors': list(debtors)})

def settings(request):
    return render_to_response("settings/show.html")

def pricelists_tab(request):
    pricelists = Pricelist.objects.all()
    return render_to_response("settings/tabs/pricelists.html", {'pricelists': pricelists})

def edit_pricelist(request, name):
    bad_request = False
    pricelist = Pricelist.objects.get(name=name)
    if request.method == "POST":
        form = EditPricelistForm(request.POST, instance=pricelist)
        if form.is_valid():
            form.save()
            return HttpResponse(200)
        else:
            bad_request = True
    else:
        form = EditPricelistForm(instance=pricelist)
    response = render_to_response('settings/dialogs/edit_pricelist.html',  {'form': form, 'pricelist': pricelist})
    if bad_request:
        response.status_code = 400
    return response



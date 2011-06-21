from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse

import simplejson, decimal

from inventory.models import *
from people.models import *
from sales.models import *
from forms import *
from models import *
from django.contrib.sites.models import Site



# utility functions

class DecimalEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


# actual views

def homepage(request):
    outstock = Product.objects.raw("select * from inventory_product where quantity < min_quantity order by name collate nocase")
    open_batchloads = BatchLoad.objects.filter(loaded = False)
    last_receipts = Scontrino.objects.order_by("-date")[:5]
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

def shop_tab(request):
    try:
        shop = Shop.objects.get(site = Site.objects.get_current())
    except:
        shop = Shop(site = Site.objects.get_current())
    bad_request = False
    if request.method == "POST":
        form = ShopForm(request.POST, instance = shop)
        if form.is_valid():
            form.save()
        else:
            bad_request = True
    else:
        form = ShopForm(instance = shop)
    response = render_to_response('settings/tabs/shop.html', {'form': form})
    if bad_request:
        response.status_code = 400
    return response

def other_tab(request):
    try:
        other_settings = Settings.objects.get(site = Site.objects.get_current())
    except:
        other_settings = Settings(site = Site.objects.get_current())
    bad_request = False
    if request.method == "POST":
        form = OtherSettingsForm(request.POST, instance = other_settings)
        if form.is_valid():
            form.save()
        else:
            bad_request = True
    else:
        form = OtherSettingsForm(instance = other_settings)
    response = render_to_response('settings/tabs/other.html', {'form': form})
    if bad_request:
        response.status_code = 400
    return response

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



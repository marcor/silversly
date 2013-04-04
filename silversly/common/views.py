from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.conf import settings

from forms import *

from people.models import *
from inventory.models import *
from sales.models import *

import simplejson
import decimal
from datetime import date

from django import http
from django.template.loader import get_template
from django.template import Context
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
import cgi




# utility functions

class DecimalEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def write_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(
        html.encode("iso-8859-1")), result)
    if not pdf.err:
        return http.HttpResponse(result.getvalue(), \
             mimetype='application/pdf')
    return http.HttpResponse('Errore nella generazione del pdf!\n %s' % cgi.escape(html))

# actual views

def homepage(request):
    outstock = Product.objects.raw("select * from inventory_product where quantity < min_quantity order by name collate nocase")
    #open_batchloads = BatchLoad.objects.filter(loaded = False)
    last_receipts = Scontrino.objects.order_by("-date")[:5]
    last_ddts = Ddt.objects.all()[:3]
    open_ddts = Ddt.objects.filter(invoice__isnull = True).select_related("cart", "cart__customer")
    customers = {}
    for ddt in open_ddts:
        customer = ddt.cart.customer
        if customer in customers:
            customers[customer] += ddt.cart.discounted_total()
        else:
            customers[customer] = ddt.cart.discounted_total()

    last_invoices = Invoice.objects.all()[:3]
    debtors = Customer.objects.raw("select * from people_customer where due > 0 collate nocase")

    return render_to_response("home.html",
        {'outstock': list(outstock),
        #'open_batchloads': open_batchloads,
        'last_receipts': last_receipts,
        'last_ddts': last_ddts,
        'need_invoice': customers,
        'last_invoices': last_invoices,
        'debtors': list(debtors)})

def show_settings(request):
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

def updates_tab(request):
    return render_to_response('settings/tabs/updates.html')

def check_updates(request):
    bad_request = False
    latest_version = get_latest_version()
    if not latest_version:
        # service unavailable
        return HttpResponse(status = 503)
    if Decimal(latest_version) > Decimal(settings.VERSION):
        # okay, there is an update
        return HttpResponse(status = 200)
    else:
        # nothing new
        return HttpResponse(status = 404)

def get_latest_version():
    try:
        remote_file = settings.LATEST_VERSION_FILE
    except:
        remote_file = None
    if remote_file:
        import urllib2
        return urllib2.urlopen(remote_file).read().strip()
    else:
        return None

def backup(request):
    location = settings.DATABASES["default"]["NAME"]
    from cStringIO import StringIO
    import zipfile
    file = StringIO()
    zf = zipfile.ZipFile(file, mode='w', compression=zipfile.ZIP_DEFLATED)
    zf.write(location, os.path.basename(location))
    zf.close()
    response = HttpResponse(file.getvalue(), mimetype="application/zip")
    response['Content-Disposition'] = 'attachment; filename=%s.zip' % date.today().strftime("%Y-%m-%d")
    return response

def update_silversly(request):
    program = os.path.join(settings.PROJECT_DIR, "script", "checkout.bat")
    # supply the proper input values as strings
    tag = get_latest_version()
    media_dir = os.path.join(settings.PROJECT_DIR, "media")
    import subprocess
    subprocess.call([program, settings.REPO_DIR, settings.REPO_NAME, tag, media_dir, settings.LIVE_MEDIA_ROOT, settings.WSGI_SCRIPT], shell=True)
    # eventually restart the apache process
    import ctypes
    ctypes.windll.libhttpd.ap_signal_parent(1)
    return HttpResponse(status = 200)

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



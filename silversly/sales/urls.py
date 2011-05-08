from django.conf.urls.defaults import *

urlpatterns = patterns('sales.views',
    url(r'carrello', 'new_receipt', name='new_receipt'),
    
    url(r'scontrino/(\d+)/$', 'edit_receipt', name='edit_receipt'),
    
    url(r'archivio/scontrino/(\d+)/$', 'show_receipt', name='show_receipt'),

)

from django.conf.urls.defaults import *

urlpatterns = patterns('sales.views',
    url(r'carrello', 'new_receipt', name='new_receipt'),
    
    url(r'scontrino/(\d+)/$', 'edit_receipt', name='edit_receipt'),
    url(r'archivio/scontrino/(\d+)/$', 'show_receipt', name='show_receipt'),
    url(r'archivio/scontrino/(\d+)/salva/$', 'save_receipt', name='save_receipt'),
    
    url(r'^cappello/aggiungi_articolo', 'add_product_to_cart', name='add_product_to_cart'),
    url(r'^cappello/rimuovi_articolo/(\d+)', 'remove_product_from_cart', name='remove_product_from_cart'),
    
    

)

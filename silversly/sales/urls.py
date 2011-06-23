from django.conf.urls.defaults import *

urlpatterns = patterns('sales.views',
    url(r'carrello$', 'edit_cart', name='edit_cart'),

    url(r'scontrino/nuovo$', 'new_receipt', name='new_receipt'),
    url(r'scontrino/(\d+)/salda$', 'pay_due_receipt', name='pay_due_receipt'),
    url(r'archivio/scontrino/(\d+)/$', 'show_receipt', name='show_receipt'),
    #url(r'archivio/scontrino/(\d+)/salva/$', 'save_receipt', name='save_receipt'),

    url(r'carrello/aggiungi_articolo', 'add_product_to_cart', name='add_product_to_cart'),
    url(r'carrello/rimuovi_articolo/(\d+)', 'remove_product_from_cart', name='remove_product_from_cart'),

    url(r'carrello/cambia_arrotondamento', 'toggle_cart_rounding', name = 'toggle_cart_rounding'),
    url(r'carrello/cambia_cliente', 'edit_cart_customer', name='edit_cart_customer'),
    url(r'carrello/cambia_sconto', 'edit_cart_discount', name='edit_cart_discount'),
    url(r'carrello/cambia_listino', 'edit_cart_pricelist', name='edit_cart_pricelist'),
    url(r'carrello/totali', 'get_cart_summary', name='get_cart_summary'),
    url(r'carrello/ricalcola', 'reload_cart', name='reload_cart'),

    url(r'ddt/nuovo$', 'new_ddt', name='new_ddt'),
    url(r'archivio/ddt/(\d+)/stampa$', 'print_ddt', name='print_ddt'),
    url(r'archivio/ddt/(\d+)/$', 'show_ddt', name='show_ddt'),
)

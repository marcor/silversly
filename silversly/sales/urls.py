from django.conf.urls.defaults import *

urlpatterns = patterns('sales.views',
    url(r'carrello$', 'edit_cart', name='edit_cart'),
    url(r'carrello/(\d+)/$', 'edit_cart', name='revise_cart'),
    
    url(r'carrello/(\d+)/nuovo_scontrino$', 'new_receipt', name='new_receipt'),
    url(r'scontrino/(\d+)/salda$', 'pay_due_receipt', name='pay_due_receipt'),
    url(r'archivio/scontrino/(\d+)/$', 'show_receipt', name='show_receipt'),
    #url(r'archivio/scontrino/(\d+)/salva/$', 'save_receipt', name='save_receipt'),

    url(r'fattura/(\d+)/salda$', 'pay_due_invoice', name='pay_due_invoice'),
    url(r'carrello/(\d+)/nuova_fattura$', 'new_invoice_from_cart', name='new_invoice_from_cart'),

    url(r'carrello/(\d+)/aggiungi_articolo', 'add_product_to_cart', name='add_product_to_cart'),
    url(r'carrello/aggiungi_articolo', 'add_product_to_cart', name='add_product_to_current_cart'),
    
    url(r'carrello/rimuovi_articolo/(\d+)', 'remove_product_from_cart', name='remove_product_from_cart'),

    url(r'carrello/(\d+)/cambia_arrotondamento', 'toggle_cart_rounding', name = 'toggle_cart_rounding'),
    url(r'carrello/(\d+)/cambia_cliente', 'edit_cart_customer', name='edit_cart_customer'),
    url(r'carrello/(\d+)/cambia_sconto', 'edit_cart_discount', name='edit_cart_discount'),
    url(r'carrello/(\d+)/cambia_listino', 'edit_cart_pricelist', name='edit_cart_pricelist'),
    
    url(r'carrello/totali$', 'get_cart_summary', name='get_current_cart_summary'),
    url(r'carrello/totali/json', 'get_cart_summary', name='get_current_cart_json_summary', kwargs={'json': True }),
    
    url(r'carrello/(\d+)/totali$', 'get_cart_summary', name='get_cart_summary'),
    url(r'carrello/(\d+)/totali/json', 'get_cart_summary', name='get_cart_json_summary', kwargs={'json': True }),
    
    url(r'carrello/(\d+)/ricalcola', 'reload_cart', name='reload_cart'),
    url(r'carrello/(\d+)/sospendi', 'suspend_cart', name='suspend_cart'),
    url(r'carrello/(\d+)/aggiungi_sospesi', 'merge_suspended', name='merge_suspended'),

    url(r'carrello/(\d+)/nuovo_ddt$', 'new_ddt', name='new_ddt'),
    url(r'archivio/ddt/(\d+)/stampa$', 'print_ddt', name='print_ddt'),
    url(r'archivio/fattura/(\d+)/stampa$', 'print_invoice', name='print_invoice'),
    url(r'archivio/fattura/(\d+)/stampa/no-ddt/$', 'print_invoice', name='print_unreferenced_invoice', kwargs={'reference_ddts': False }),
    url(r'archivio/ddt/(\d+)/$', 'show_ddt', name='show_ddt'),
    url(r'archivio/fattura/(\d+)/$', 'show_invoice', name='show_invoice'),
    url(r'archivio/fattura/annulla_ultima/$', 'delete_invoice', name='delete_last_invoice'),
)

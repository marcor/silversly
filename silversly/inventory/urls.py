from django.conf.urls.defaults import *
from forms import CategoryForm, ChildCategoryForm

urlpatterns = patterns('inventory.views',
    url(r'articolo/(\d+)/$', 'show_product', name='show_product'),
    url(r'articolo/(\d+)/tab/principale', 'product_tab', name='product_tab'),
    url(r'articolo/(\d+)/tab/prezzi', 'prices_tab', name='prices_tab'),
    url(r'articolo/(\d+)/tab/movimenti', 'history_tab', name='history_tab'),
    
    url(r'articolo/(\d+)/fornitore/aggiungi', 'add_supply', name='add_supply'),
    url(r'articolo/(\d+)/fornitori/$', 'list_supplies', name='list_supplies'),
    url(r'articolo/(\d+)/fornitori/readonly/', 'list_supplies', name='list_supplies_readonly', kwargs={'simple': True}),
    
    url(r'articolo/(\d+)/listini/', 'list_prices', name='list_prices'),
    url(r'articolo/(\d+)/listino/(.+)/modifica', 'modify_price', name='modify_price'),
    url(r'prezzo/(\d+)/rimuovi/', 'reset_price', name='reset_price'),
    
    url(r'articolo/carica', 'load_products', name='load_products'),
    
    url(r'fornitura/(\d+)/modifica', 'modify_supply', name='modify_supply'),
    url(r'fornitura/(\d+)/elimina', 'remove_supply', name='remove_supply'),
    
    
    url(r'articolo/aggiungi/', 'add_product', name='add_product'),
    url(r'articolo/(\d+)/elimina/', 'delete_product', name='delete_product'),
    
    
    url(r'articolo/cerca/$', 'find_product', name='find_product'),
    url(r'articolo/cerca/ajax/', 'ajax_find_product', name='ajax_find_product'),
    url(r'articolo/(\d+)/prezzi_listino/(.+)/ajax/', 'ajax_get_prices', name='ajax_get_prices'),
    
    url(r'vendite/carrello/', 'show_cart', name='show_cart'),
   
    url(r'fornitore/cerca/', 'find_supplier', name='find_supplier'),
    
    url(r'fornitore/(\d+)/$', 'show_supplier', name='show_supplier'),
    url(r'fornitore/aggiungi/', 'add_supplier', name='add_supplier'),
    
    url(r'fornitore/(\d+)/tab/principale', 'supplier_info_tab', name='supplier_info_tab'),
    url(r'fornitore/(\d+)/tab/forniture', 'supplier_history_tab', name='supplier_history_tab'),
    
    url(r'cliente/cerca/$', 'find_customer', name='find_customer'),
    url(r'cliente/(\d+)/$', 'show_customer', name='show_customer'),
    url(r'cliente/aggiungi/', 'add_customer', name='add_customer'),
    
    url(r'cliente/(\d+)/tab/principale', 'customer_info_tab', name='customer_info_tab'),
    url(r'cliente/(\d+)/tab/acquisti', 'customer_history_tab', name='customer_history_tab'),
    
    url(r'categorie/', 'list_categories', name='list_categories'),
    url(r'categoria/(\d+)', 'list_by_category', name='list_by_category'),
    url(r'categoria/aggiungi', 'add_category', name='add_category', kwargs={'formclass': CategoryForm}),
    url(r'categoria/(\d+)/aggiungi', 'add_category', name='add_child_category', kwargs={'formclass': ChildCategoryForm}),
    
    url(r'carrello/aggiungi_articolo/(\d+)', 'add_to_cart', name='add_to_cart')
)

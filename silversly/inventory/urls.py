from django.conf.urls.defaults import *
from forms import CategoryForm, ChildCategoryForm

urlpatterns = patterns('inventory.views',
    url(r'^(\d+)/$', 'show_product', name='show_product'),
    url(r'^infobox', 'show_infobox', name='show_infobox'),
    url(r'^(\d+)/tab/principale', 'product_tab', name='product_tab'),
    url(r'^(\d+)/tab/prezzi', 'prices_tab', name='prices_tab'),
    url(r'^(\d+)/tab/movimenti', 'history_tab', name='history_tab'),
    url(r'^(\d+)/tab/extra', 'product_extra_tab', name='product_extra_tab'),

    url(r'^(\d+)/cambia_fattore', 'save_product_factor', name='save_product_factor'),

    url(r'^(\d+)/fornitore/aggiungi', 'add_supply', name='add_supply'),
    url(r'^(\d+)/fornitori/$', 'list_supplies', name='list_supplies'),
    url(r'^(\d+)/fornitori/readonly/', 'list_supplies_readonly', name='list_supplies_readonly'),

    url(r'^(\d+)/listini/', 'list_prices', name='list_prices'),
    url(r'^temp/listini/', 'list_temp_prices', name='list_temp_prices'),
    url(r'^(\d+)/listino/(.+)/modifica', 'modify_price', name='modify_price'),
    url(r'^prezzo/(\d+)/rimuovi/', 'reset_price', name='reset_price'),
    url(r'^temp/(\d+)/listino/(.+)/modifica', 'modify_temp_price', name='modify_temp_price'),
    url(r'^temp/prezzo/(\d+)/rimuovi/', 'reset_temp_price', name='reset_temp_price'),

    url(r'^carica', 'load_products', name='load_products'),

    url(r'^fornitura/(\d+)/modifica', 'modify_supply', name='modify_supply'),
    url(r'^fornitura/(\d+)/elimina', 'remove_supply', name='remove_supply'),

    url(r'^rifornimento/nuovo', 'new_batch_load', name='new_batch_load'),
    url(r'^rifornimento/(\d+)$', 'show_batch_load', name='show_batch_load'),
    url(r'^rifornimento/(\d+)/aggiungi_articolo', 'add_product_to_batch', name='add_product_to_batch'),
    url(r'^rifornimento/(\d+)/rimuovi_articolo/(\d+)', 'remove_product_from_batch', name='remove_product_from_batch'),
    url(r'^rifornimento/(\d+)/save', 'save_batch_load', name='save_batch_load'),

    url(r'^aggiungi/', 'add_product', name='add_product'),
    url(r'^(\d+)/elimina/', 'delete_product', name='delete_product'),

    url(r'^cerca/$', 'find_product', name='find_product'),
    url(r'^cerca/ajax/', 'ajax_find_product', name='ajax_find_product'),
    url(r'^(\d+)/cerca_denom/', 'ajax_find_denominator', name='ajax_find_denominator'),
    url(r'^(\d+)/prezzi_listino/(.+)/ajax/', 'ajax_get_prices', name='ajax_get_prices'),

    url(r'^categorie/$', 'list_categories', name='list_categories'),
    url(r'^categorie/pdf/', 'products_to_pdf', name='products_to_pdf'),
    url(r'^categorie/xls/', 'products_to_xls', name='products_to_xls'),
    url(r'^categoria/(\d+)', 'list_by_category', name='list_by_category'),
    url(r'^categoria/aggiungi', 'add_category', name='add_category', kwargs={'formclass': CategoryForm}),
    url(r'^categoria/(\d+)/aggiungi', 'add_category', name='add_child_category', kwargs={'formclass': ChildCategoryForm}),

    url(r'^catalogo$', 'print_catalogue', name='print_catalogue'),

    url(r'^quickedit', 'ajax_quickedit', name='quickedit'),
    url(r'^(\d+)/update', 'ajax_mark_up_to_date', name='ajax_mark_up_to_date'),
)

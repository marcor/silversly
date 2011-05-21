from django.conf.urls.defaults import *

urlpatterns = patterns('people.views',
    url(r'fornitore/cerca/', 'find_supplier', name='find_supplier'),

    url(r'fornitore/(\d+)/$', 'show_supplier', name='show_supplier'),
    url(r'fornitore/aggiungi/', 'add_supplier', name='add_supplier'),

    url(r'fornitore/(\d+)/tab/principale', 'supplier_info_tab', name='supplier_info_tab'),
    url(r'fornitore/(\d+)/tab/forniture', 'supplier_history_tab', name='supplier_history_tab'),

    url(r'cliente/cerca/$', 'find_customer', name='find_customer'),
    url(r'cliente/cerca/ajax/', 'ajax_find_customer', name='ajax_find_customer'),
    url(r'cliente/(\d+)/$', 'show_customer', name='show_customer'),
    url(r'privato/aggiungi/', 'add_customer', name='add_customer'),
    url(r'azienda/aggiungi/', 'add_company', name='add_company'),

    url(r'cliente/(\d+)/tab/principale', 'customer_info_tab', name='customer_info_tab'),
    url(r'cliente/(\d+)/tab/commerciale', 'customer_commercial_tab', name='customer_commercial_tab'),
    url(r'cliente/(\d+)/tab/acquisti', 'customer_history_tab', name='customer_history_tab'),
)

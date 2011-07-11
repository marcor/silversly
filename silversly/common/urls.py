from django.conf.urls.defaults import *

urlpatterns = patterns('common.views',
    url(r'^$', 'show_settings', name='settings'),
    url(r'^pricelists/$', 'pricelists_tab', name='pricelists_tab'),
    url(r'^pricelists/(.+)/edit$', 'edit_pricelist', name='edit_pricelist'),

    url(r'^updates/$', 'updates_tab', name='updates_tab'),
    url(r'^updates/installa$', 'update_silversly', name='update_silversly'),
    url(r'^updates/controlla$', 'check_updates', name='check_updates'),
    url(r'^shop/$', 'shop_tab', name='shop_tab'),
    url(r'^other/$', 'other_tab', name='other_tab'),
    
    url(r'^backup$', 'backup', name='backup'),
    
)

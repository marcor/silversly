from django.conf.urls.defaults import *

urlpatterns = patterns('common.views',
    url(r'^$', 'settings', name='settings'),
    url(r'^pricelists/$', 'pricelists_tab', name='pricelists_tab'),
    url(r'^pricelists/(.+)/edit$', 'edit_pricelist', name='edit_pricelist'),

    url(r'^shop/$', 'shop_tab', name='shop_tab'),
    url(r'^other/$', 'other_tab', name='other_tab'),

)

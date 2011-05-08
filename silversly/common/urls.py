from django.conf.urls.defaults import *

urlpatterns = patterns('common.views',
    url(r'^$', 'settings', name='settings'),
    url(r'^pricelists/$', 'pricelists_tab', name='pricelists_tab'),
    url(r'^pricelists/(.+)/edit$', 'edit_pricelist', name='edit_pricelist'),

)

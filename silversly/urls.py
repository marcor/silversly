from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^$', 'common.views.homepage', name="homepage"),
    url(r'^articoli/', include('inventory.urls')),
    url(r'^anagrafica/', include('people.urls')),
    url(r'^vendite/', include('sales.urls')),
    #(r'', include('inventory.urls')),    
)


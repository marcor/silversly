from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #(r'^posi/', include('posi.inventory.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/marcor/projects/python/.virtualenvs/test/silversly/media'}),
    url(r'^$', 'inventory.views.find_product'),
    (r'', include('inventory.urls')),
    
)


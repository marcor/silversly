from django.contrib import admin
from models import *

admin.site.register(Category)
admin.site.register(Pricelist)
admin.site.register(Price)
admin.site.register(Product)
admin.site.register(Supply)

# todo: move to separate app
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Receipt)
admin.site.register(Invoice)
admin.site.register(Ddt)

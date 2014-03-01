from django.core.management.base import BaseCommand
from django.db.models import loading
from django.core.serializers import serialize
from django.conf import settings
from django.template import Variable, VariableDoesNotExist

from inventory.models import Product, Category
from datetime import date
from decimal import Decimal

class Command(BaseCommand):
    help = 'Randomly trim the inventory to match max value'
    args = "[max_value]"

    def handle(self, max_value, **options):
        import random
        
        ps = Product.objects.filter(base_price__gt = 0, quantity__gt = 0)
        max_value = Decimal(max_value)
        
        inventory_value = Decimal("0.00")
        
        for p in ps:  
            p.total_value = p.get_total_value()
            inventory_value += p.total_value
        
        trim_value = inventory_value - max_value
        
        print inventory_value, max_value
        
        i = 0
        while trim_value > 0:
            for p in ps:
                old_total = p.get_total_value()
                p.quantity = int(p.quantity) and random.randrange(int(p.quantity)  + 1) 
                new_total = p.get_total_value()
                trim_value -= old_total - new_total
                if trim_value > 0:
                    print trim_value, i
                    i += 1
                else:
                    break
        print trim_value, i
        
        for i in range(len(ps)):
            ps[i].save()
            if i % 100 == 0:
                print i
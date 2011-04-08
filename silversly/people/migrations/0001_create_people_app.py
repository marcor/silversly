# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('inventory_customer', 'people_customer') 
        db.rename_table('inventory_retailcustomer', 'people_retailcustomer')
        db.rename_table('inventory_supplier', 'people_supplier')
        db.rename_table('inventory_bank', 'people_bank')
        db.rename_table('inventory_address', 'people_address')

    def backwards(self, orm):
        
        db.rename_table('people_customer', 'inventory_customer') 
        db.rename_table('people_retailcustomer', 'inventory_retailcustomer')
        db.rename_table('people_supplier', 'inventory_supplier')
        db.rename_table('people_bank', 'inventory_bank')
        db.rename_table('people_address', 'inventory_address')

    complete_apps = ['people']

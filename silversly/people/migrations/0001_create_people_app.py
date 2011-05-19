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

    models = {
        'people.address': {
            'Meta': {'object_name': 'Address'},
            'street' : ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
        },
        'people.bank': {
            'Meta': {'object_name': 'Bank'},
            'abi': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'cab': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'people.retailcustomer': {
            'Meta': {'object_name': 'RetailCustomer'},
            'due': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'email': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '15', 'blank': 'True'})
        },
        'people.supplier': {
            'Meta': {'ordering': "['name']", 'object_name': 'Supplier'},
            'email': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '15', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '15', 'blank': 'True'})
        },
        'people.customer': {
            'Meta': {'object_name': 'Customer'},
            'bank': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['people.Bank']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'costs': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'}),
            'email': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_address': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '15', 'blank': 'True'}),
            'shipping_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['people']

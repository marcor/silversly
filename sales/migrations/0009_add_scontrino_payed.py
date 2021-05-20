# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Scontrino.payed'
        db.add_column('sales_scontrino', 'payed', self.gf('common.models.FixedDecimalField')(default=0, max_digits=7, decimal_places=2), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Scontrino.payed'
        db.delete_column('sales_scontrino', 'payed')


    models = {
        'inventory.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Category']", 'null': 'True', 'blank': 'True'})
        },
        'inventory.price': {
            'Meta': {'unique_together': "(('pricelist', 'product'),)", 'object_name': 'Price'},
            'gross': ('common.models.FixedDecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'markup': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'net': ('common.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
            'pricelist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Pricelist']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Product']"})
        },
        'inventory.pricelist': {
            'Meta': {'object_name': 'Pricelist'},
            'default_markup': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'default_method': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'primary_key': 'True'})
        },
        'inventory.product': {
            'Meta': {'ordering': "['name', 'code']", 'object_name': 'Product'},
            'base_price': ('common.models.FixedDecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'catalogue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Category']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_quantity': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'prices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.Pricelist']", 'null': 'True', 'through': "orm['inventory.Price']", 'symmetrical': 'False'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['people.Supplier']", 'null': 'True', 'through': "orm['inventory.Supply']", 'symmetrical': 'False'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'inventory.supply': {
            'Meta': {'unique_together': "(('product', 'supplier'),)", 'object_name': 'Supply'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('common.models.FixedDecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Product']"}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Supplier']"}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'people.bank': {
            'Meta': {'object_name': 'Bank'},
            'abi': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'cab': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'people.customer': {
            'Meta': {'object_name': 'Customer'},
            'cf': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'discount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'due': ('common.models.FixedDecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'pricelist': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Pubblico'", 'to': "orm['inventory.Pricelist']"})
        },
        'people.supplier': {
            'Meta': {'ordering': "['name']", 'object_name': 'Supplier'},
            'email': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '15', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '15', 'blank': 'True'})
        },
        'sales.cart': {
            'Meta': {'object_name': 'Cart'},
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Customer']", 'null': 'True'}),
            'discount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'final_discount': ('common.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
            'final_total': ('common.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pricelist': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Pubblico'", 'to': "orm['inventory.Pricelist']"}),
            'rounded': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'sales.cartitem': {
            'Meta': {'object_name': 'CartItem'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.Cart']"}),
            'discount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'final_discount': ('common.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
            'final_price': ('common.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
            'final_value': ('common.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Product']"}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'update': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'sales.ddt': {
            'Meta': {'ordering': "['date', 'number']", 'object_name': 'Ddt', '_ormbases': ['sales.Receipt']},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'main_address': ('django.db.models.fields.TextField', [], {}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'receipt_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sales.Receipt']", 'unique': 'True', 'primary_key': 'True'}),
            'shipping_address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'shipping_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 5, 21, 14, 58, 33, 491932)'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'sales.invoice': {
            'Meta': {'object_name': 'Invoice', '_ormbases': ['sales.Receipt']},
            'bank': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['people.Bank']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'costs': ('common.models.FixedDecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'immediate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'receipt_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sales.Receipt']", 'unique': 'True', 'primary_key': 'True'}),
            'receipts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'proxy_receipt'", 'null': 'True', 'to': "orm['sales.Receipt']"}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'sales.receipt': {
            'Meta': {'object_name': 'Receipt'},
            'cart': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sales.Cart']", 'unique': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sales.scontrino': {
            'Meta': {'object_name': 'Scontrino', '_ormbases': ['sales.Receipt']},
            'cf': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'unique': 'True', 'blank': 'True'}),
            'due': ('common.models.FixedDecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'}),
            'payed': ('common.models.FixedDecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'receipt_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sales.Receipt']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['sales']

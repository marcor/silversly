# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'CartItem.cart'
        db.add_column('inventory_cartitem', 'cart', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['inventory.Cart']), keep_default=False)

        # Removing M2M table for field products on 'Cart'
        db.delete_table('inventory_cart_products')


    def backwards(self, orm):
        
        # Deleting field 'CartItem.cart'
        db.delete_column('inventory_cartitem', 'cart_id')

        # Adding M2M table for field products on 'Cart'
        db.create_table('inventory_cart_products', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cart', models.ForeignKey(orm['inventory.cart'], null=False)),
            ('cartitem', models.ForeignKey(orm['inventory.cartitem'], null=False))
        ))
        db.create_unique('inventory_cart_products', ['cart_id', 'cartitem_id'])


    models = {
        'inventory.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'inventory.bank': {
            'Meta': {'object_name': 'Bank'},
            'abi': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'cab': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'inventory.cart': {
            'Meta': {'ordering': "['date']", 'object_name': 'Cart'},
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'inventory.cartitem': {
            'Meta': {'object_name': 'CartItem'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Cart']"}),
            'discount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Product']"}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'update': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'inventory.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Category']", 'null': 'True', 'blank': 'True'})
        },
        'inventory.customer': {
            'Meta': {'object_name': 'Customer'},
            'bank': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['inventory.Bank']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'costs': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'}),
            'email': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_address': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '15', 'blank': 'True'}),
            'shipping_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'inventory.ddt': {
            'Meta': {'ordering': "['date', 'number']", 'object_name': 'Ddt'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Cart']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.RetailCustomer']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_address': ('django.db.models.fields.TextField', [], {}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'}),
            'shipping_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'shipping_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 13, 11, 47, 59, 908000)'})
        },
        'inventory.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'bank': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['inventory.Bank']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'costs': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'}),
            'ddts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.Ddt']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'inventory.logentry': {
            'Meta': {'object_name': 'LogEntry'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '3'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Product']"}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Supplier']", 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'inventory.markup': {
            'Meta': {'unique_together': "(('pricelist', 'product'),)", 'object_name': 'Markup'},
            'charge': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pricelist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Pricelist']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Product']"})
        },
        'inventory.pricelist': {
            'Meta': {'object_name': 'Pricelist'},
            'default_markup': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'primary_key': 'True'}),
            'rounding': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'inventory.product': {
            'Meta': {'object_name': 'Product'},
            'base_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Category']"}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '13'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'markups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.Pricelist']", 'null': 'True', 'through': "orm['inventory.Markup']", 'symmetrical': 'False'}),
            'min_quantity': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.Supplier']", 'null': 'True', 'through': "orm['inventory.Supply']", 'symmetrical': 'False'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'inventory.receipt': {
            'Meta': {'object_name': 'Receipt'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Cart']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.RetailCustomer']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'inventory.retailcustomer': {
            'Meta': {'object_name': 'RetailCustomer'},
            'due': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'email': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '15', 'blank': 'True'})
        },
        'inventory.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'email': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '15', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '15', 'blank': 'True'})
        },
        'inventory.supply': {
            'Meta': {'unique_together': "(('product', 'supplier'),)", 'object_name': 'Supply'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Product']"}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Supplier']"}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['inventory']

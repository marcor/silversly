# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'Product', fields ['code']
        db.delete_unique('inventory_product', ['code'])

        # Adding model 'BatchLoad'
        db.create_table('inventory_batchload', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(related_name='product_batch', to=orm['inventory.Supplier'])),
            ('document_ref', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('inventory', ['BatchLoad'])

        # Adding model 'IncomingProduct'
        db.create_table('inventory_incomingproduct', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('actual_product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Product'], null=True, blank=True)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.BatchLoad'])),
            ('quantity', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=3)),
            ('new_supplier_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('new_supplier_price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3)),
        ))
        db.send_create_signal('inventory', ['IncomingProduct'])

        # Adding unique constraint on 'IncomingProduct', fields ['batch', 'actual_product']
        db.create_unique('inventory_incomingproduct', ['batch_id', 'actual_product_id'])

        # Adding model 'NewPrice'
        db.create_table('inventory_newprice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2)),
            ('markup', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True)),
            ('pricelist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Pricelist'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.IncomingProduct'])),
        ))
        db.send_create_signal('inventory', ['NewPrice'])

        # Adding unique constraint on 'NewPrice', fields ['pricelist', 'product']
        db.create_unique('inventory_newprice', ['pricelist_id', 'product_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'NewPrice', fields ['pricelist', 'product']
        db.delete_unique('inventory_newprice', ['pricelist_id', 'product_id'])

        # Removing unique constraint on 'IncomingProduct', fields ['batch', 'actual_product']
        db.delete_unique('inventory_incomingproduct', ['batch_id', 'actual_product_id'])

        # Deleting model 'BatchLoad'
        db.delete_table('inventory_batchload')

        # Deleting model 'IncomingProduct'
        db.delete_table('inventory_incomingproduct')

        # Deleting model 'NewPrice'
        db.delete_table('inventory_newprice')

        # Adding unique constraint on 'Product', fields ['code']
        db.create_unique('inventory_product', ['code'])


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
        'inventory.batchload': {
            'Meta': {'object_name': 'BatchLoad'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'document_ref': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product_batch'", 'to': "orm['inventory.Supplier']"})
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
            'shipping_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 14, 0, 59, 49, 355414)'})
        },
        'inventory.incomingproduct': {
            'Meta': {'unique_together': "(['batch', 'actual_product'],)", 'object_name': 'IncomingProduct'},
            'actual_product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Product']", 'null': 'True', 'blank': 'True'}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.BatchLoad']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_prices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.Pricelist']", 'null': 'True', 'through': "orm['inventory.NewPrice']", 'symmetrical': 'False'}),
            'new_supplier_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'new_supplier_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'})
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
        'inventory.newprice': {
            'Meta': {'unique_together': "(('pricelist', 'product'),)", 'object_name': 'NewPrice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'markup': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'pricelist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Pricelist']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.IncomingProduct']"}),
            'value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'})
        },
        'inventory.price': {
            'Meta': {'unique_together': "(('pricelist', 'product'),)", 'object_name': 'Price'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'markup': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'pricelist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Pricelist']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Product']"}),
            'value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'})
        },
        'inventory.pricelist': {
            'Meta': {'object_name': 'Pricelist'},
            'default_markup': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'default_method': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'primary_key': 'True'})
        },
        'inventory.product': {
            'Meta': {'ordering': "['name', 'code']", 'object_name': 'Product'},
            'base_price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Category']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_quantity': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'prices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.Pricelist']", 'null': 'True', 'through': "orm['inventory.Price']", 'symmetrical': 'False'}),
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

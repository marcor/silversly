# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RetailCustomer'
        db.create_table('inventory_retailcustomer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('due', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=3)),
            ('phone', self.gf('django.db.models.fields.CharField')(default=None, max_length=15, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(default=None, max_length=30, blank=True)),
        ))
        db.send_create_signal('inventory', ['RetailCustomer'])

        # Adding model 'Receipt'
        db.create_table('inventory_receipt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Cart'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.RetailCustomer'], null=True, blank=True)),
        ))
        db.send_create_signal('inventory', ['Receipt'])

        # Adding model 'Invoice'
        db.create_table('inventory_invoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveSmallIntegerField')(unique=True)),
            ('payment_method', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('bank', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['inventory.Bank'], unique=True, null=True, blank=True)),
            ('costs', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=7, decimal_places=2)),
        ))
        db.send_create_signal('inventory', ['Invoice'])

        # Adding M2M table for field ddts on 'Invoice'
        db.create_table('inventory_invoice_ddts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('invoice', models.ForeignKey(orm['inventory.invoice'], null=False)),
            ('ddt', models.ForeignKey(orm['inventory.ddt'], null=False))
        ))
        db.create_unique('inventory_invoice_ddts', ['invoice_id', 'ddt_id'])

        # Adding model 'Ddt'
        db.create_table('inventory_ddt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveSmallIntegerField')(unique=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Cart'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.RetailCustomer'], null=True, blank=True)),
            ('main_address', self.gf('django.db.models.fields.TextField')()),
            ('shipping_address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('shipping_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 2, 13, 10, 41, 17, 987000))),
        ))
        db.send_create_signal('inventory', ['Ddt'])

        # Adding model 'CartItem'
        db.create_table('inventory_cartitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Product'])),
            ('quantity', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('discount', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('update', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('inventory', ['CartItem'])

        # Adding model 'Cart'
        db.create_table('inventory_cart', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('current', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('inventory', ['Cart'])

        # Adding M2M table for field products on 'Cart'
        db.create_table('inventory_cart_products', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cart', models.ForeignKey(orm['inventory.cart'], null=False)),
            ('cartitem', models.ForeignKey(orm['inventory.cartitem'], null=False))
        ))
        db.create_unique('inventory_cart_products', ['cart_id', 'cartitem_id'])

        # Adding field 'Customer.main_address'
        db.add_column('inventory_customer', 'main_address', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding field 'Customer.shipping_address'
        db.add_column('inventory_customer', 'shipping_address', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Customer.costs'
        db.add_column('inventory_customer', 'costs', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=7, decimal_places=2), keep_default=False)

        # Deleting field 'Bank.iban'
        db.delete_column('inventory_bank', 'iban')

        # Adding field 'Bank.abi'
        db.add_column('inventory_bank', 'abi', self.gf('django.db.models.fields.CharField')(default='', max_length=5), keep_default=False)

        # Adding field 'Bank.cab'
        db.add_column('inventory_bank', 'cab', self.gf('django.db.models.fields.CharField')(default='', max_length=5), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'RetailCustomer'
        db.delete_table('inventory_retailcustomer')

        # Deleting model 'Receipt'
        db.delete_table('inventory_receipt')

        # Deleting model 'Invoice'
        db.delete_table('inventory_invoice')

        # Removing M2M table for field ddts on 'Invoice'
        db.delete_table('inventory_invoice_ddts')

        # Deleting model 'Ddt'
        db.delete_table('inventory_ddt')

        # Deleting model 'CartItem'
        db.delete_table('inventory_cartitem')

        # Deleting model 'Cart'
        db.delete_table('inventory_cart')

        # Removing M2M table for field products on 'Cart'
        db.delete_table('inventory_cart_products')

        # Deleting field 'Customer.main_address'
        db.delete_column('inventory_customer', 'main_address')

        # Deleting field 'Customer.shipping_address'
        db.delete_column('inventory_customer', 'shipping_address')

        # Deleting field 'Customer.costs'
        db.delete_column('inventory_customer', 'costs')

        # Adding field 'Bank.iban'
        db.add_column('inventory_bank', 'iban', self.gf('django.db.models.fields.CharField')(default='', max_length=27), keep_default=False)

        # Deleting field 'Bank.abi'
        db.delete_column('inventory_bank', 'abi')

        # Deleting field 'Bank.cab'
        db.delete_column('inventory_bank', 'cab')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.CartItem']", 'symmetrical': 'False'})
        },
        'inventory.cartitem': {
            'Meta': {'object_name': 'CartItem'},
            'discount': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
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
            'shipping_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 13, 10, 44, 31, 614000)'})
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

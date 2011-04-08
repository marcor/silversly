# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    depends_on = (
        ('people', '0001_create_people_app'),
    )
    
    def forwards(self, orm):

        # Changing field 'BatchLoad.supplier'
        db.alter_column('inventory_batchload', 'supplier_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['people.Supplier']))

        # Changing field 'Supply.price'
        db.alter_column('inventory_supply', 'price', self.gf('inventory.models.FixedDecimalField')(max_digits=8, decimal_places=3))

        # Changing field 'Supply.supplier'
        db.alter_column('inventory_supply', 'supplier_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Supplier']))

        # Changing field 'Receipt.customer'
        db.alter_column('inventory_receipt', 'customer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.RetailCustomer'], null=True))

        # Changing field 'IncomingProduct.new_base_price'
        db.alter_column('inventory_incomingproduct', 'new_base_price', self.gf('inventory.models.FixedDecimalField')(max_digits=8, decimal_places=3))

        # Changing field 'IncomingProduct.new_supplier_price'
        db.alter_column('inventory_incomingproduct', 'new_supplier_price', self.gf('inventory.models.FixedDecimalField')(max_digits=8, decimal_places=3))

        # Changing field 'IncomingProduct.quantity'
        db.alter_column('inventory_incomingproduct', 'quantity', self.gf('inventory.models.FixedDecimalField')(max_digits=8, decimal_places=3))

        # Changing field 'Invoice.costs'
        db.alter_column('inventory_invoice', 'costs', self.gf('inventory.models.FixedDecimalField')(max_digits=7, decimal_places=2))

        # Changing field 'Invoice.bank'
        db.alter_column('inventory_invoice', 'bank_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['people.Bank'], unique=True, null=True))

        # Changing field 'Ddt.customer'
        db.alter_column('inventory_ddt', 'customer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.RetailCustomer'], null=True))

        # Changing field 'CartItem.quantity'
        db.alter_column('inventory_cartitem', 'quantity', self.gf('inventory.models.FixedDecimalField')(max_digits=7, decimal_places=2))

        # Changing field 'Price.gross'
        db.alter_column('inventory_price', 'gross', self.gf('inventory.models.FixedDecimalField')(max_digits=7, decimal_places=2))

        # Changing field 'Price.net'
        db.alter_column('inventory_price', 'net', self.gf('inventory.models.FixedDecimalField')(null=True, max_digits=7, decimal_places=2))

        # Changing field 'LogEntry.price'
        db.alter_column('inventory_logentry', 'price', self.gf('inventory.models.FixedDecimalField')(null=True, max_digits=8, decimal_places=3))

        # Changing field 'LogEntry.supplier'
        db.alter_column('inventory_logentry', 'supplier_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Supplier'], null=True))

        # Changing field 'LogEntry.quantity'
        db.alter_column('inventory_logentry', 'quantity', self.gf('inventory.models.FixedDecimalField')(max_digits=8, decimal_places=3))

        # Changing field 'Product.min_quantity'
        db.alter_column('inventory_product', 'min_quantity', self.gf('inventory.models.FixedDecimalField')(max_digits=8, decimal_places=3))

        # Changing field 'Product.quantity'
        db.alter_column('inventory_product', 'quantity', self.gf('inventory.models.FixedDecimalField')(max_digits=8, decimal_places=3))

        # Changing field 'Product.base_price'
        db.alter_column('inventory_product', 'base_price', self.gf('inventory.models.FixedDecimalField')(max_digits=8, decimal_places=3))

        # Changing field 'NewPrice.value'
        db.alter_column('inventory_newprice', 'value', self.gf('inventory.models.FixedDecimalField')(null=True, max_digits=7, decimal_places=2))


    def backwards(self, orm):

        # Changing field 'BatchLoad.supplier'
        db.alter_column('inventory_batchload', 'supplier_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['inventory.Supplier']))

        # Changing field 'Supply.price'
        db.alter_column('inventory_supply', 'price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3))

        # Changing field 'Supply.supplier'
        db.alter_column('inventory_supply', 'supplier_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Supplier']))

        # Changing field 'Receipt.customer'
        db.alter_column('inventory_receipt', 'customer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.RetailCustomer'], null=True))

        # Changing field 'IncomingProduct.new_base_price'
        db.alter_column('inventory_incomingproduct', 'new_base_price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3))

        # Changing field 'IncomingProduct.new_supplier_price'
        db.alter_column('inventory_incomingproduct', 'new_supplier_price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3))

        # Changing field 'IncomingProduct.quantity'
        db.alter_column('inventory_incomingproduct', 'quantity', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3))

        # Changing field 'Invoice.costs'
        db.alter_column('inventory_invoice', 'costs', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2))

        # Changing field 'Invoice.bank'
        db.alter_column('inventory_invoice', 'bank_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['inventory.Bank'], unique=True, null=True))

        # Changing field 'Ddt.customer'
        db.alter_column('inventory_ddt', 'customer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.RetailCustomer'], null=True))

        # Changing field 'CartItem.quantity'
        db.alter_column('inventory_cartitem', 'quantity', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2))

        # Changing field 'Price.gross'
        db.alter_column('inventory_price', 'gross', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2))

        # Changing field 'Price.net'
        db.alter_column('inventory_price', 'net', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2))

        # Changing field 'LogEntry.price'
        db.alter_column('inventory_logentry', 'price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=3))

        # Changing field 'LogEntry.supplier'
        db.alter_column('inventory_logentry', 'supplier_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Supplier'], null=True))

        # Changing field 'LogEntry.quantity'
        db.alter_column('inventory_logentry', 'quantity', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3))

        # Changing field 'Product.min_quantity'
        db.alter_column('inventory_product', 'min_quantity', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3))

        # Changing field 'Product.quantity'
        db.alter_column('inventory_product', 'quantity', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3))

        # Changing field 'Product.base_price'
        db.alter_column('inventory_product', 'base_price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3))

        # Changing field 'NewPrice.value'
        db.alter_column('inventory_newprice', 'value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2))


    models = {
        'inventory.batchload': {
            'Meta': {'object_name': 'BatchLoad'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'document_ref': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product_batch'", 'null': 'True', 'to': "orm['people.Supplier']"})
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
            'quantity': ('inventory.models.FixedDecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'update': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'inventory.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Category']", 'null': 'True', 'blank': 'True'})
        },
        'inventory.ddt': {
            'Meta': {'ordering': "['date', 'number']", 'object_name': 'Ddt'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Cart']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.RetailCustomer']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_address': ('django.db.models.fields.TextField', [], {}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'}),
            'shipping_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'shipping_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 4, 8, 23, 24, 14, 306570)'})
        },
        'inventory.incomingproduct': {
            'Meta': {'unique_together': "(['batch', 'actual_product'],)", 'object_name': 'IncomingProduct'},
            'actual_product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Product']", 'null': 'True', 'blank': 'True'}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.BatchLoad']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_base_price': ('inventory.models.FixedDecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'new_prices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.Pricelist']", 'null': 'True', 'through': "orm['inventory.NewPrice']", 'symmetrical': 'False'}),
            'new_supplier_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'new_supplier_price': ('inventory.models.FixedDecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'quantity': ('inventory.models.FixedDecimalField', [], {'max_digits': '8', 'decimal_places': '3'})
        },
        'inventory.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'bank': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['people.Bank']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'costs': ('inventory.models.FixedDecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'}),
            'ddts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.Ddt']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'inventory.logentry': {
            'Meta': {'object_name': 'LogEntry'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('inventory.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '3'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Product']"}),
            'quantity': ('inventory.models.FixedDecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Supplier']", 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'inventory.newprice': {
            'Meta': {'unique_together': "(('pricelist', 'product'),)", 'object_name': 'NewPrice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'markup': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'pricelist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Pricelist']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.IncomingProduct']"}),
            'value': ('inventory.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'})
        },
        'inventory.price': {
            'Meta': {'unique_together': "(('pricelist', 'product'),)", 'object_name': 'Price'},
            'gross': ('inventory.models.FixedDecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'markup': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'net': ('inventory.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
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
            'base_price': ('inventory.models.FixedDecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Category']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_quantity': ('inventory.models.FixedDecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'prices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.Pricelist']", 'null': 'True', 'through': "orm['inventory.Price']", 'symmetrical': 'False'}),
            'quantity': ('inventory.models.FixedDecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['people.Supplier']", 'null': 'True', 'through': "orm['inventory.Supply']", 'symmetrical': 'False'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'inventory.receipt': {
            'Meta': {'object_name': 'Receipt'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Cart']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.RetailCustomer']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'inventory.supply': {
            'Meta': {'unique_together': "(('product', 'supplier'),)", 'object_name': 'Supply'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('inventory.models.FixedDecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
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
        }
    }

    complete_apps = ['inventory']

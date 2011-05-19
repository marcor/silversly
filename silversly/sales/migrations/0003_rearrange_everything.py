# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    depends_on = (
        ('people', '0002_fix_customer_models_remove_address'),
    )
    
    def forwards(self, orm):
        
        # Removing M2M table for field ddts on 'Invoice'
        db.delete_table('inventory_invoice_ddts')

        # Removing unique constraint on 'Ddt', fields ['number']
        db.delete_unique('sales_ddt', ['number'])

        # Removing unique constraint on 'Receipt', fields ['number', 'year']
        db.delete_unique('sales_receipt', ['number', 'year'])

        # Removing unique constraint on 'Invoice', fields ['number']
        db.delete_unique('sales_invoice', ['number'])

        # Adding model 'Scontrino'
        db.create_table('sales_scontrino', (
            ('receipt_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sales.Receipt'], unique=True, primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, unique=True, blank=True)),
            ('due', self.gf('common.models.FixedDecimalField')(max_digits=7, decimal_places=2)),
            ('cf', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal('sales', ['Scontrino'])

        # Adding field 'Cart.discount'
        db.add_column('sales_cart', 'discount', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0), keep_default=False)

        # Adding field 'Cart.rounded'
        db.add_column('sales_cart', 'rounded', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Cart.final_total'
        db.add_column('sales_cart', 'final_total', self.gf('common.models.FixedDecimalField')(null=True, max_digits=7, decimal_places=2), keep_default=False)

        # Adding field 'Cart.final_discount'
        db.add_column('sales_cart', 'final_discount', self.gf('common.models.FixedDecimalField')(null=True, max_digits=7, decimal_places=2), keep_default=False)

        # Adding field 'CartItem.final_price'
        db.add_column('sales_cartitem', 'final_price', self.gf('common.models.FixedDecimalField')(null=True, max_digits=7, decimal_places=2), keep_default=False)

        # Adding field 'CartItem.final_discount'
        db.add_column('sales_cartitem', 'final_discount', self.gf('common.models.FixedDecimalField')(null=True, max_digits=7, decimal_places=2), keep_default=False)

        # Adding field 'Invoice.year'
        db.add_column('sales_invoice', 'year', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=11), keep_default=False)

        # Adding field 'Invoice.immediate'
        db.add_column('sales_invoice', 'immediate', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Invoice.cart'
        db.add_column('sales_invoice', 'cart', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sales.Cart'], unique=True, null=True), keep_default=False)

        # Adding M2M table for field receipts on 'Invoice'
        db.create_table('sales_invoice_receipts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('invoice', models.ForeignKey(orm['sales.invoice'], null=False)),
            ('receipt', models.ForeignKey(orm['sales.receipt'], null=False))
        ))
        db.create_unique('sales_invoice_receipts', ['invoice_id', 'receipt_id'])

        # Deleting field 'Receipt.customer'
        db.delete_column('sales_receipt', 'customer_id')

        # Deleting field 'Receipt.number'
        db.delete_column('sales_receipt', 'number')

        # Deleting field 'Receipt.year'
        db.delete_column('sales_receipt', 'year')

        # Deleting field 'Receipt.date'
        db.delete_column('sales_receipt', 'date')

        # Deleting field 'Ddt.customer'
        db.delete_column('sales_ddt', 'customer_id')

        # Deleting field 'Ddt.id'
        db.delete_column('sales_ddt', 'id')

        # Deleting field 'Ddt.cart'
        db.delete_column('sales_ddt', 'cart_id')

        # Adding field 'Ddt.receipt_ptr'
        db.add_column('sales_ddt', 'receipt_ptr', self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['sales.Receipt'], unique=True, primary_key=True), keep_default=False)

        # Adding field 'Ddt.year'
        db.add_column('sales_ddt', 'year', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=11), keep_default=False)

        # Changing field 'Ddt.shipping_address'
        db.alter_column('sales_ddt', 'shipping_address', self.gf('django.db.models.fields.TextField')(default=''))


    def backwards(self, orm):
        
        # Deleting model 'Scontrino'
        db.delete_table('sales_scontrino')

        # Deleting model 'InvoiceItem'
        db.delete_table('sales_invoiceitem')

        # Deleting field 'Cart.discount'
        db.delete_column('sales_cart', 'discount')

        # Deleting field 'Cart.rounded'
        db.delete_column('sales_cart', 'rounded')

        # Deleting field 'Cart.final_total'
        db.delete_column('sales_cart', 'final_total')

        # Deleting field 'Cart.final_discount'
        db.delete_column('sales_cart', 'final_discount')

        # Deleting field 'CartItem.final_price'
        db.delete_column('sales_cartitem', 'final_price')

        # Deleting field 'CartItem.final_discount'
        db.delete_column('sales_cartitem', 'final_discount')

        # Deleting field 'Invoice.year'
        db.delete_column('sales_invoice', 'year')

        # Deleting field 'Invoice.immediate'
        db.delete_column('sales_invoice', 'immediate')

        # Deleting field 'Invoice.cart'
        db.delete_column('sales_invoice', 'cart_id')

        # Adding M2M table for field ddts on 'Invoice'
        db.create_table('sales_invoice_ddts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('invoice', models.ForeignKey(orm['sales.invoice'], null=False)),
            ('ddt', models.ForeignKey(orm['sales.ddt'], null=False))
        ))
        db.create_unique('sales_invoice_ddts', ['invoice_id', 'ddt_id'])

        # Removing M2M table for field receipts on 'Invoice'
        db.delete_table('sales_invoice_receipts')

        # Adding unique constraint on 'Invoice', fields ['number']
        db.create_unique('sales_invoice', ['number'])

        # Adding field 'Receipt.customer'
        db.add_column('sales_receipt', 'customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.RetailCustomer'], null=True, blank=True), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'Receipt.number'
        raise RuntimeError("Cannot reverse this migration. 'Receipt.number' and its values cannot be restored.")

        # Adding field 'Receipt.year'
        db.add_column('sales_receipt', 'year', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=11), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'Receipt.date'
        raise RuntimeError("Cannot reverse this migration. 'Receipt.date' and its values cannot be restored.")

        # Adding unique constraint on 'Receipt', fields ['number', 'year']
        db.create_unique('sales_receipt', ['number', 'year'])

        # Adding field 'Ddt.customer'
        db.add_column('sales_ddt', 'customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.RetailCustomer'], null=True, blank=True), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'Ddt.id'
        raise RuntimeError("Cannot reverse this migration. 'Ddt.id' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Ddt.cart'
        raise RuntimeError("Cannot reverse this migration. 'Ddt.cart' and its values cannot be restored.")

        # Deleting field 'Ddt.receipt_ptr'
        db.delete_column('sales_ddt', 'receipt_ptr_id')

        # Deleting field 'Ddt.year'
        db.delete_column('sales_ddt', 'year')

        # Adding unique constraint on 'Ddt', fields ['number']
        db.create_unique('sales_ddt', ['number'])

        # Changing field 'Ddt.shipping_address'
        db.alter_column('sales_ddt', 'shipping_address', self.gf('django.db.models.fields.TextField')(null=True))


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
            'discount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'final_discount': ('common.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
            'final_total': ('common.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rounded': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'sales.cartitem': {
            'Meta': {'object_name': 'CartItem'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.Cart']"}),
            'discount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'final_discount': ('common.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
            'final_price': ('common.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
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
            'shipping_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 5, 19, 21, 12, 57, 894049)'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'sales.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'bank': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['people.Bank']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'cart': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sales.Cart']", 'unique': 'True', 'null': 'True'}),
            'costs': ('common.models.FixedDecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'immediate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'receipts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sales.Receipt']", 'null': 'True', 'symmetrical': 'False'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'sales.receipt': {
            'Meta': {'object_name': 'Receipt'},
            'cart': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sales.Cart']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sales.scontrino': {
            'Meta': {'object_name': 'Scontrino', '_ormbases': ['sales.Receipt']},
            'cf': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'unique': 'True', 'blank': 'True'}),
            'due': ('common.models.FixedDecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'receipt_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sales.Receipt']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['sales']

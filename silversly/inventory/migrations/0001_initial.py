# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('inventory_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Category'], null=True, blank=True)),
        ))
        db.send_create_signal('inventory', ['Category'])

        # Adding model 'Bank'
        db.create_table('inventory_bank', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('iban', self.gf('django.db.models.fields.CharField')(max_length=27)),
        ))
        db.send_create_signal('inventory', ['Bank'])

        # Adding model 'Address'
        db.create_table('inventory_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('inventory', ['Address'])

        # Adding model 'Supplier'
        db.create_table('inventory_supplier', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('phone', self.gf('django.db.models.fields.CharField')(default=None, max_length=15, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(default=None, max_length=30, blank=True)),
        ))
        db.send_create_signal('inventory', ['Supplier'])

        # Adding model 'Customer'
        db.create_table('inventory_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('phone', self.gf('django.db.models.fields.CharField')(default=None, max_length=15, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(default=None, max_length=30, blank=True)),
            ('payment_method', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('bank', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['inventory.Bank'], unique=True, null=True)),
        ))
        db.send_create_signal('inventory', ['Customer'])

        # Adding model 'Pricelist'
        db.create_table('inventory_pricelist', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25, primary_key=True)),
            ('default_markup', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('inventory', ['Pricelist'])

        # Adding model 'Product'
        db.create_table('inventory_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=13)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('quantity', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=3)),
            ('min_quantity', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=3)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Category'])),
            ('base_price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=3)),
        ))
        db.send_create_signal('inventory', ['Product'])

        # Adding model 'Markup'
        db.create_table('inventory_markup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('charge', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('pricelist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Pricelist'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Product'])),
        ))
        db.send_create_signal('inventory', ['Markup'])

        # Adding unique constraint on 'Markup', fields ['pricelist', 'product']
        db.create_unique('inventory_markup', ['pricelist_id', 'product_id'])

        # Adding model 'LogEntry'
        db.create_table('inventory_logentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Product'])),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Supplier'], null=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=3)),
            ('quantity', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('inventory', ['LogEntry'])

        # Adding model 'Supply'
        db.create_table('inventory_supply', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Product'])),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Supplier'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3)),
            ('updated', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('inventory', ['Supply'])

        # Adding unique constraint on 'Supply', fields ['product', 'supplier']
        db.create_unique('inventory_supply', ['product_id', 'supplier_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Supply', fields ['product', 'supplier']
        db.delete_unique('inventory_supply', ['product_id', 'supplier_id'])

        # Removing unique constraint on 'Markup', fields ['pricelist', 'product']
        db.delete_unique('inventory_markup', ['pricelist_id', 'product_id'])

        # Deleting model 'Category'
        db.delete_table('inventory_category')

        # Deleting model 'Bank'
        db.delete_table('inventory_bank')

        # Deleting model 'Address'
        db.delete_table('inventory_address')

        # Deleting model 'Supplier'
        db.delete_table('inventory_supplier')

        # Deleting model 'Customer'
        db.delete_table('inventory_customer')

        # Deleting model 'Pricelist'
        db.delete_table('inventory_pricelist')

        # Deleting model 'Product'
        db.delete_table('inventory_product')

        # Deleting model 'Markup'
        db.delete_table('inventory_markup')

        # Deleting model 'LogEntry'
        db.delete_table('inventory_logentry')

        # Deleting model 'Supply'
        db.delete_table('inventory_supply')


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
            'iban': ('django.db.models.fields.CharField', [], {'max_length': '27'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'inventory.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Category']", 'null': 'True', 'blank': 'True'})
        },
        'inventory.customer': {
            'Meta': {'object_name': 'Customer'},
            'bank': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['inventory.Bank']", 'unique': 'True', 'null': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'email': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '15', 'blank': 'True'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'primary_key': 'True'})
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
        'inventory.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'email': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30', 'blank': 'True'}),
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

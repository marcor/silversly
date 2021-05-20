# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'LogEntry.supplier'
        db.delete_column('inventory_logentry', 'supplier_id')

        # Deleting field 'LogEntry.price'
        db.delete_column('inventory_logentry', 'price')

        # Deleting field 'LogEntry.type'
        db.delete_column('inventory_logentry', 'type')


    def backwards(self, orm):
        
        # Adding field 'LogEntry.supplier'
        db.add_column('inventory_logentry', 'supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Supplier'], null=True), keep_default=False)

        # Adding field 'LogEntry.price'
        db.add_column('inventory_logentry', 'price', self.gf('common.models.FixedDecimalField')(null=True, max_digits=8, decimal_places=3), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'LogEntry.type'
        raise RuntimeError("Cannot reverse this migration. 'LogEntry.type' and its values cannot be restored.")


    models = {
        'inventory.batchload': {
            'Meta': {'object_name': 'BatchLoad'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'document_ref': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product_batch'", 'null': 'True', 'to': "orm['people.Supplier']"})
        },
        'inventory.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Category']", 'null': 'True', 'blank': 'True'})
        },
        'inventory.incomingproduct': {
            'Meta': {'unique_together': "(['batch', 'actual_product'],)", 'object_name': 'IncomingProduct'},
            'actual_product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Product']", 'null': 'True', 'blank': 'True'}),
            'base_price': ('common.models.FixedDecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.BatchLoad']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_prices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.Pricelist']", 'null': 'True', 'through': "orm['inventory.NewPrice']", 'symmetrical': 'False'}),
            'new_supplier_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'new_supplier_price': ('common.models.FixedDecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'})
        },
        'inventory.logentry': {
            'Meta': {'object_name': 'LogEntry'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Product']"}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'})
        },
        'inventory.newprice': {
            'Meta': {'unique_together': "(('pricelist', 'product'),)", 'object_name': 'NewPrice'},
            'gross': ('common.models.FixedDecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'markup': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'net': ('common.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
            'pricelist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Pricelist']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.IncomingProduct']"}),
            'reset_pricelist_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
            'denominator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'multiple_set'", 'null': 'True', 'to': "orm['inventory.Product']"}),
            'factor': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
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
            'altprice': ('common.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '3', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('common.models.FixedDecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Product']"}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Supplier']"}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
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

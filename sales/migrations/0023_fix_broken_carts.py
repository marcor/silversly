# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        newcart = orm.Cart(customer=orm['people.Customer'].objects.get(name__startswith = "AMMINISTRAZIONE COMUNALE"),  current=False, suspended=True)
        newcart.save()
        invoiced_cart = orm.Cart.objects.get(id=17731)
        invoiced_cart.current = False
        sold_later = invoiced_cart.cartitem_set.all()[:17]
        for item in sold_later:
            item.cart = newcart
            item.save()
        for item in invoiced_cart.cartitem_set.all()[1:3]:
            item.cart = newcart
            item.save()
        #newcart.update_value()
        newcart.save()
        #invoiced_cart.update_value()
        invoiced_cart.save()

    def backwards(self, orm):
        "Write your backwards methods here."
        raise RuntimeError("Cannot reverse this migration.")

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
            'denominator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'multiple_set'", 'null': 'True', 'to': "orm['inventory.Product']"}),
            'factor': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_quantity': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'prices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.Pricelist']", 'null': 'True', 'through': "orm['inventory.Price']", 'symmetrical': 'False'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '3'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['people.Supplier']", 'null': 'True', 'through': "orm['inventory.Supply']", 'symmetrical': 'False'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
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
            'final_net_discount': ('common.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
            'final_net_total': ('common.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
            'final_total': ('common.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pricelist': ('django.db.models.fields.related.ForeignKey', [], {'default': "'Pubblico'", 'to': "orm['inventory.Pricelist']"}),
            'rounded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vat_rate': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '22'})
        },
        'sales.cartitem': {
            'Meta': {'ordering': "['-id']", 'object_name': 'CartItem'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.Cart']"}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'discount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'final_net_price': ('common.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
            'final_price': ('common.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Product']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'update': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'sales.ddt': {
            'Meta': {'ordering': "['-year', '-date', '-number']", 'object_name': 'Ddt', '_ormbases': ['sales.Receipt']},
            'appearance': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'boxes': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sales.Invoice']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'main_address': ('django.db.models.fields.TextField', [], {}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'receipt_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sales.Receipt']", 'unique': 'True', 'primary_key': 'True'}),
            'shipping_address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'shipping_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 2, 29, 0, 0)'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '16'})
        },
        'sales.invoice': {
            'Meta': {'ordering': "['-year', '-date', '-number']", 'object_name': 'Invoice', '_ormbases': ['sales.Receipt']},
            'costs': ('common.models.FixedDecimalField', [], {'default': "'3.10'", 'max_digits': '7', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2016, 2, 29, 0, 0)'}),
            'immediate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'payed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'receipt_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sales.Receipt']", 'unique': 'True', 'primary_key': 'True'}),
            'total_net': ('common.models.FixedDecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'vat_rate': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '22'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '16'})
        },
        'sales.painvoice': {
            'Meta': {'ordering': "['-year', '-date', '-number']", 'object_name': 'PAInvoice', '_ormbases': ['sales.Invoice']},
            'cig': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'invoice_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sales.Invoice']", 'unique': 'True', 'primary_key': 'True'}),
            'refdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'refdoc': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        'sales.receipt': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Receipt'},
            'cart': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sales.Cart']", 'unique': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sales.scontrino': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Scontrino', '_ormbases': ['sales.Receipt']},
            'cf': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'unique': 'True', 'blank': 'True'}),
            'due': ('common.models.FixedDecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'}),
            'payed': ('common.models.FixedDecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'receipt_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sales.Receipt']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['sales']
    symmetrical = True

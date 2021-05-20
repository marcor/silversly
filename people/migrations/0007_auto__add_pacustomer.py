# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PACustomer'
        db.create_table('people_pacustomer', (
            ('companycustomer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['people.CompanyCustomer'], unique=True, primary_key=True)),
            ('cu', self.gf('django.db.models.fields.CharField')(unique=True, max_length=6)),
        ))
        db.send_create_signal('people', ['PACustomer'])


    def backwards(self, orm):
        # Deleting model 'PACustomer'
        db.delete_table('people_pacustomer')


    models = {
        'inventory.pricelist': {
            'Meta': {'object_name': 'Pricelist'},
            'default_markup': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'default_method': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'primary_key': 'True'})
        },
        'people.bank': {
            'Meta': {'object_name': 'Bank'},
            'abi': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'cab': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'people.companycustomer': {
            'Meta': {'object_name': 'CompanyCustomer', '_ormbases': ['people.Customer']},
            'bank': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['people.Bank']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'costs': ('common.models.FixedDecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'}),
            'customer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['people.Customer']", 'unique': 'True', 'primary_key': 'True'}),
            'main_address': ('django.db.models.fields.TextField', [], {}),
            'payment_method': ('django.db.models.fields.CharField', [], {'default': "'30fm'", 'max_length': '4'}),
            'piva': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'shipping_address': ('django.db.models.fields.TextField', [], {'blank': 'True'})
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
        'people.pacustomer': {
            'Meta': {'object_name': 'PACustomer', '_ormbases': ['people.CompanyCustomer']},
            'companycustomer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['people.CompanyCustomer']", 'unique': 'True', 'primary_key': 'True'}),
            'cu': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6'})
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

    complete_apps = ['people']
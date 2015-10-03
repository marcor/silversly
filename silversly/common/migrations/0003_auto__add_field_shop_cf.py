# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Shop.cf'
        db.add_column('common_shop', 'cf',
                      self.gf('django.db.models.fields.CharField')(default='MNTSVN66P44G337A', max_length=16),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Shop.cf'
        db.delete_column('common_shop', 'cf')


    models = {
        'common.settings': {
            'Meta': {'object_name': 'Settings'},
            'close_receipts': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receipt_folder': ('django.db.models.fields.CharField', [], {'default': "'c:\\\\Scontrini'", 'max_length': '60'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True'})
        },
        'common.shop': {
            'Meta': {'object_name': 'Shop'},
            'bank': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'cf': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'iban': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_address': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'piva': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['common']
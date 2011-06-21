# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Shop'
        db.create_table('common_shop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sites.Site'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('piva', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('main_address', self.gf('django.db.models.fields.TextField')()),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('bank', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('iban', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('common', ['Shop'])

        # Adding model 'Settings'
        db.create_table('common_settings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sites.Site'], unique=True)),
            ('close_receipts', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('receipt_folder', self.gf('django.db.models.fields.CharField')(default='c:\\Scontrini', max_length=60)),
        ))
        db.send_create_signal('common', ['Settings'])


    def backwards(self, orm):
        
        # Deleting model 'Shop'
        db.delete_table('common_shop')

        # Deleting model 'Settings'
        db.delete_table('common_settings')


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

# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    depends_on = (
        ('sales', '0002_auto__del_field_cart_date__add_field_receipt_year__chg_field_receipt_c'),
    )
    
    def forwards(self, orm):
        
        # Deleting model 'Address'
        db.delete_table('people_address')

        # Deleting model 'RetailCustomer'
        db.delete_table('people_retailcustomer')

        # Adding model 'CompanyCustomer'
        db.create_table('people_companycustomer', (
            ('customer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['people.Customer'], unique=True, primary_key=True)),
            ('piva', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('main_address', self.gf('django.db.models.fields.TextField')()),
            ('shipping_address', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('payment_method', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('bank', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['people.Bank'], unique=True, blank=True)),
            ('costs', self.gf('common.models.FixedDecimalField')(default=0, max_digits=7, decimal_places=2)),
        ))
        db.send_create_signal('people', ['CompanyCustomer'])

        # Deleting field 'Customer.code'
        db.delete_column('people_customer', 'code')

        # Deleting field 'Customer.main_address'
        db.delete_column('people_customer', 'main_address')

        # Deleting field 'Customer.payment_method'
        db.delete_column('people_customer', 'payment_method')

        # Deleting field 'Customer.bank'
        db.delete_column('people_customer', 'bank_id')

        # Deleting field 'Customer.costs'
        db.delete_column('people_customer', 'costs')

        # Deleting field 'Customer.shipping_address'
        db.delete_column('people_customer', 'shipping_address')

        # Adding field 'Customer.cf'
        db.add_column('people_customer', 'cf', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=20, blank=True), keep_default=False)

        # Adding field 'Customer.discount'
        db.add_column('people_customer', 'discount', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0), keep_default=False)

        # Adding field 'Customer.due'
        db.add_column('people_customer', 'due', self.gf('common.models.FixedDecimalField')(default=0, max_digits=8, decimal_places=2), keep_default=False)

        # Changing field 'Customer.email'
        db.alter_column('people_customer', 'email', self.gf('django.db.models.fields.EmailField')(max_length=30))


    def backwards(self, orm):
        
        # Adding model 'Address'
        db.create_table('people_address', (
            ('province', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('people', ['Address'])

        # Adding model 'RetailCustomer'
        db.create_table('people_retailcustomer', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
            ('due', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=8, decimal_places=3)),
            ('email', self.gf('django.db.models.fields.CharField')(default=None, max_length=30, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(default=None, max_length=15, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('people', ['RetailCustomer'])

        # Deleting model 'CompanyCustomer'
        db.delete_table('people_companycustomer')

        # User chose to not deal with backwards NULL issues for 'Customer.code'
        raise RuntimeError("Cannot reverse this migration. 'Customer.code' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Customer.main_address'
        raise RuntimeError("Cannot reverse this migration. 'Customer.main_address' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Customer.payment_method'
        raise RuntimeError("Cannot reverse this migration. 'Customer.payment_method' and its values cannot be restored.")

        # Adding field 'Customer.bank'
        db.add_column('people_customer', 'bank', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['people.Bank'], unique=True, null=True, blank=True), keep_default=False)

        # Adding field 'Customer.costs'
        db.add_column('people_customer', 'costs', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=7, decimal_places=2), keep_default=False)

        # Adding field 'Customer.shipping_address'
        db.add_column('people_customer', 'shipping_address', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Deleting field 'Customer.cf'
        db.delete_column('people_customer', 'cf')

        # Deleting field 'Customer.discount'
        db.delete_column('people_customer', 'discount')

        # Deleting field 'Customer.due'
        db.delete_column('people_customer', 'due')

        # Changing field 'Customer.email'
        db.alter_column('people_customer', 'email', self.gf('django.db.models.fields.CharField')(max_length=30))


    models = {
        'people.bank': {
            'Meta': {'object_name': 'Bank'},
            'abi': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'cab': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'people.companycustomer': {
            'Meta': {'object_name': 'CompanyCustomer', '_ormbases': ['people.Customer']},
            'bank': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['people.Bank']", 'unique': 'True', 'blank': 'True'}),
            'costs': ('common.models.FixedDecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '2'}),
            'customer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['people.Customer']", 'unique': 'True', 'primary_key': 'True'}),
            'main_address': ('django.db.models.fields.TextField', [], {}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'piva': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'shipping_address': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'people.customer': {
            'Meta': {'object_name': 'Customer'},
            'cf': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'blank': 'True'}),
            'discount': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'due': ('common.models.FixedDecimalField', [], {'default': '0', 'max_digits': '8', 'decimal_places': '2'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
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

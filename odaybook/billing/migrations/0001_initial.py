# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Transaction'
        db.create_table('billing_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('user_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('sum', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=2)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('billing', ['Transaction'])


    def backwards(self, orm):
        
        # Deleting model 'Transaction'
        db.delete_table('billing_transaction')


    models = {
        'billing.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sum': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {}),
            'user_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['billing']

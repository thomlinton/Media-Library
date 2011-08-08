# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Person'
        db.create_table('media_library_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('residence', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('born_on', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('media_library', ['Person'])

        # Adding model 'Device'
        db.create_table('media_library_device', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('type', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('media_library', ['Device'])


    def backwards(self, orm):
        
        # Deleting model 'Person'
        db.delete_table('media_library_person')

        # Deleting model 'Device'
        db.delete_table('media_library_device')


    models = {
        'media_library.device': {
            'Meta': {'object_name': 'Device'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'media_library.person': {
            'Meta': {'object_name': 'Person'},
            'born_on': ('django.db.models.fields.DateField', [], {}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'residence': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['media_library']

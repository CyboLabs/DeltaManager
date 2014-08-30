# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Owner'
        db.create_table('common_owner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, related_name='user')),
        ))
        db.send_create_signal('common', ['Owner'])

        # Adding model 'Manufacturer'
        db.create_table('common_manufacturer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('common', ['Manufacturer'])

        # Adding model 'Device'
        db.create_table('common_device', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code_name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Manufacturer'], related_name='manufacturer')),
        ))
        db.send_create_signal('common', ['Device'])

        # Adding model 'File'
        db.create_table('common_file', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Owner'], related_name='owner')),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Device'], related_name='device')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('version', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=20)),
            ('size', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('download_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('md5sum', self.gf('api.v1.common.fields.Md5SumField')()),
            ('old_version', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=20)),
        ))
        db.send_create_signal('common', ['File'])

        # Adding model 'RequestUpload'
        db.create_table('common_requestupload', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Owner'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Device'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('version', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=20)),
            ('old_version', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=20)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('common', ['RequestUpload'])


    def backwards(self, orm):
        # Deleting model 'Owner'
        db.delete_table('common_owner')

        # Deleting model 'Manufacturer'
        db.delete_table('common_manufacturer')

        # Deleting model 'Device'
        db.delete_table('common_device')

        # Deleting model 'File'
        db.delete_table('common_file')

        # Deleting model 'RequestUpload'
        db.delete_table('common_requestupload')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Group']", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'common.device': {
            'Meta': {'object_name': 'Device'},
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Manufacturer']", 'related_name': "'manufacturer'"})
        },
        'common.file': {
            'Meta': {'object_name': 'File'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Device']", 'related_name': "'device'"}),
            'download_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5sum': ('api.v1.common.fields.Md5SumField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'old_version': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '20'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Owner']", 'related_name': "'owner'"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'version': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '20'})
        },
        'common.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'common.owner': {
            'Meta': {'object_name': 'Owner'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'related_name': "'user'"})
        },
        'common.requestupload': {
            'Meta': {'object_name': 'RequestUpload'},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Device']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'old_version': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '20'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Owner']"}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'version': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '20'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['common']
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UsalRingTimetable'
        db.create_table('attendance_usalringtimetable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('start', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.School'])),
            ('workday', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('attendance', ['UsalRingTimetable'])

        # Adding model 'SpecicalRingTimetable'
        db.create_table('attendance_specicalringtimetable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('start', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.School'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('attendance', ['SpecicalRingTimetable'])

        # Adding model 'UsalTimetable'
        db.create_table('attendance_usaltimetable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rest_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('grade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.Grade'])),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.Subject'])),
            ('room', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.School'])),
            ('workday', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('attendance', ['UsalTimetable'])

        # Adding model 'SpecicalTimetable'
        db.create_table('attendance_specicaltimetable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rest_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('grade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.Grade'])),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.Subject'])),
            ('room', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.School'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('attendance', ['SpecicalTimetable'])

        # Adding model 'Holiday'
        db.create_table('attendance_holiday', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.School'])),
        ))
        db.send_create_signal('attendance', ['Holiday'])


    def backwards(self, orm):
        
        # Deleting model 'UsalRingTimetable'
        db.delete_table('attendance_usalringtimetable')

        # Deleting model 'SpecicalRingTimetable'
        db.delete_table('attendance_specicalringtimetable')

        # Deleting model 'UsalTimetable'
        db.delete_table('attendance_usaltimetable')

        # Deleting model 'SpecicalTimetable'
        db.delete_table('attendance_specicaltimetable')

        # Deleting model 'Holiday'
        db.delete_table('attendance_holiday')


    models = {
        'attendance.holiday': {
            'Meta': {'object_name': 'Holiday'},
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.School']"}),
            'start': ('django.db.models.fields.DateField', [], {})
        },
        'attendance.specicalringtimetable': {
            'Meta': {'object_name': 'SpecicalRingTimetable'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.School']"}),
            'start': ('django.db.models.fields.TimeField', [], {})
        },
        'attendance.specicaltimetable': {
            'Meta': {'ordering': "['number']", 'object_name': 'SpecicalTimetable'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'grade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Grade']"}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'rest_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.School']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Subject']"})
        },
        'attendance.usalringtimetable': {
            'Meta': {'object_name': 'UsalRingTimetable'},
            'end': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.School']"}),
            'start': ('django.db.models.fields.TimeField', [], {}),
            'workday': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'attendance.usaltimetable': {
            'Meta': {'ordering': "['number']", 'object_name': 'UsalTimetable'},
            'grade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Grade']"}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'rest_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.School']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Subject']"}),
            'workday': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'userextended.grade': {
            'Meta': {'ordering': "['number']", 'object_name': 'Grade'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'rest_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.School']"}),
            'small_name': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'userextended.school': {
            'Meta': {'object_name': 'School'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gapps_domain': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gapps_login': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gapps_password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gapps_use': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_mark': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'private_domain': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'private_salute': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'rest_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'userextended.subject': {
            'Meta': {'ordering': "['name']", 'object_name': 'Subject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rest_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.School']"})
        }
    }

    complete_apps = ['attendance']

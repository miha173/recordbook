# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Lesson'
        db.create_table('marks_lesson', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rest_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.Teacher'], null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('task', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.Subject'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('marks', ['Lesson'])

        # Adding M2M table for field grade on 'Lesson'
        db.create_table('marks_lesson_grade', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lesson', models.ForeignKey(orm['marks.lesson'], null=False)),
            ('grade', models.ForeignKey(orm['userextended.grade'], null=False))
        ))
        db.create_unique('marks_lesson_grade', ['lesson_id', 'grade_id'])

        # Adding model 'Mark'
        db.create_table('marks_mark', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rest_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('pupil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.Pupil'])),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['marks.Lesson'])),
            ('mark', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('absent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('marks', ['Mark'])

        # Adding model 'ResultDate'
        db.create_table('marks_resultdate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rest_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.School'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('period', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('startdate', self.gf('django.db.models.fields.DateField')()),
            ('enddate', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('marks', ['ResultDate'])

        # Adding M2M table for field grades on 'ResultDate'
        db.create_table('marks_resultdate_grades', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('resultdate', models.ForeignKey(orm['marks.resultdate'], null=False)),
            ('grade', models.ForeignKey(orm['userextended.grade'], null=False))
        ))
        db.create_unique('marks_resultdate_grades', ['resultdate_id', 'grade_id'])

        # Adding model 'Result'
        db.create_table('marks_result', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rest_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('resultdate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['marks.ResultDate'])),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.Subject'])),
            ('pupil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.Pupil'])),
            ('mark', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('marks', ['Result'])


    def backwards(self, orm):
        
        # Deleting model 'Lesson'
        db.delete_table('marks_lesson')

        # Removing M2M table for field grade on 'Lesson'
        db.delete_table('marks_lesson_grade')

        # Deleting model 'Mark'
        db.delete_table('marks_mark')

        # Deleting model 'ResultDate'
        db.delete_table('marks_resultdate')

        # Removing M2M table for field grades on 'ResultDate'
        db.delete_table('marks_resultdate_grades')

        # Deleting model 'Result'
        db.delete_table('marks_result')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('codename',)", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'marks.lesson': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Lesson'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'grade': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['userextended.Grade']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rest_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Subject']"}),
            'task': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Teacher']", 'null': 'True', 'blank': 'True'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'marks.mark': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Mark'},
            'absent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marks.Lesson']"}),
            'mark': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pupil': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Pupil']"}),
            'rest_modified': ('django.db.models.fields.DateTimeField', [], {})
        },
        'marks.result': {
            'Meta': {'object_name': 'Result'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mark': ('django.db.models.fields.IntegerField', [], {}),
            'pupil': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Pupil']"}),
            'rest_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'resultdate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['marks.ResultDate']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Subject']"})
        },
        'marks.resultdate': {
            'Meta': {'ordering': "['enddate']", 'object_name': 'ResultDate'},
            'enddate': ('django.db.models.fields.DateField', [], {}),
            'grades': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['userextended.Grade']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'period': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'rest_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.School']"}),
            'startdate': ('django.db.models.fields.DateField', [], {})
        },
        'userextended.baseuser': {
            'Meta': {'object_name': 'BaseUser'},
            'cart': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'clerk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Clerk']", 'null': 'True', 'blank': 'True'}),
            'current_role': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'userextended_baseuser_related_role_related'", 'null': 'True', 'to': "orm['userextended.BaseUser']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'userextended_baseuser_related_roles_related'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['userextended.BaseUser']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'})
        },
        'userextended.clerk': {
            'Meta': {'ordering': "['last_name', 'first_name', 'middle_name']", 'object_name': 'Clerk', '_ormbases': ['auth.User']},
            'cart': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'current_role': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'userextended_clerk_related_role_related'", 'null': 'True', 'to': "orm['userextended.BaseUser']"}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'rest_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'userextended_clerk_related_roles_related'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['userextended.BaseUser']"}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
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
        'userextended.pupil': {
            'Meta': {'object_name': 'Pupil', '_ormbases': ['userextended.BaseUser']},
            'baseuser_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['userextended.BaseUser']", 'unique': 'True', 'primary_key': 'True'}),
            'grade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Grade']", 'null': 'True'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'health_group': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1', 'null': 'True'}),
            'health_note': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'insurance_policy': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'parent_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parent_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parent_phone_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parent_phone_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.School']", 'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
        },
        'userextended.teacher': {
            'Meta': {'unique_together': "(('grade',),)", 'object_name': 'Teacher', '_ormbases': ['userextended.BaseUser']},
            'baseuser_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['userextended.BaseUser']", 'unique': 'True', 'primary_key': 'True'}),
            'current_grade': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'current_grade'", 'null': 'True', 'to': "orm['userextended.Grade']"}),
            'current_subject': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'current_subject'", 'null': 'True', 'to': "orm['userextended.Subject']"}),
            'edu_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'grade': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'grade'", 'null': 'True', 'to': "orm['userextended.Grade']"}),
            'grades': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'grades'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['userextended.Grade']"}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.School']", 'null': 'True', 'blank': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'subjects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['userextended.Subject']"}),
            'tech_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['marks']

# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Test'
        db.create_table('tests_test', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='teacher', to=orm['userextended.Teacher'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.Subject'])),
            ('mark5', self.gf('django.db.models.fields.IntegerField')()),
            ('mark4', self.gf('django.db.models.fields.IntegerField')()),
            ('mark3', self.gf('django.db.models.fields.IntegerField')()),
            ('public', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('tests', ['Test'])

        # Adding M2M table for field grades on 'Test'
        db.create_table('tests_test_grades', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('test', models.ForeignKey(orm['tests.test'], null=False)),
            ('grade', models.ForeignKey(orm['userextended.grade'], null=False))
        ))
        db.create_unique('tests_test_grades', ['test_id', 'grade_id'])

        # Adding M2M table for field share on 'Test'
        db.create_table('tests_test_share', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('test', models.ForeignKey(orm['tests.test'], null=False)),
            ('teacher', models.ForeignKey(orm['userextended.teacher'], null=False))
        ))
        db.create_unique('tests_test_share', ['test_id', 'teacher_id'])

        # Adding model 'Question'
        db.create_table('tests_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tests.Test'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('tests', ['Question'])

        # Adding model 'VariantA'
        db.create_table('tests_varianta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tests.Question'])),
            ('task', self.gf('django.db.models.fields.TextField')()),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('option1', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('option2', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('option3', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('option4', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('tests', ['VariantA'])

        # Adding model 'VariantB'
        db.create_table('tests_variantb', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tests.Question'])),
            ('task', self.gf('django.db.models.fields.TextField')()),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('tests', ['VariantB'])

        # Adding model 'Result'
        db.create_table('tests_result', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pupil', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pupil', to=orm['userextended.Pupil'])),
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tests.Test'])),
            ('mark', self.gf('django.db.models.fields.IntegerField')()),
            ('questionA', self.gf('django.db.models.fields.TextField')()),
            ('questionB', self.gf('django.db.models.fields.TextField')()),
            ('answersA', self.gf('django.db.models.fields.TextField')()),
            ('answersB', self.gf('django.db.models.fields.TextField')()),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('tests', ['Result'])


    def backwards(self, orm):
        
        # Deleting model 'Test'
        db.delete_table('tests_test')

        # Removing M2M table for field grades on 'Test'
        db.delete_table('tests_test_grades')

        # Removing M2M table for field share on 'Test'
        db.delete_table('tests_test_share')

        # Deleting model 'Question'
        db.delete_table('tests_question')

        # Deleting model 'VariantA'
        db.delete_table('tests_varianta')

        # Deleting model 'VariantB'
        db.delete_table('tests_variantb')

        # Deleting model 'Result'
        db.delete_table('tests_result')


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
        'tests.question': {
            'Meta': {'object_name': 'Question'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tests.Test']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'tests.result': {
            'Meta': {'object_name': 'Result'},
            'answersA': ('django.db.models.fields.TextField', [], {}),
            'answersB': ('django.db.models.fields.TextField', [], {}),
            'end': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mark': ('django.db.models.fields.IntegerField', [], {}),
            'pupil': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pupil'", 'to': "orm['userextended.Pupil']"}),
            'questionA': ('django.db.models.fields.TextField', [], {}),
            'questionB': ('django.db.models.fields.TextField', [], {}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tests.Test']"})
        },
        'tests.test': {
            'Meta': {'object_name': 'Test'},
            'grades': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['userextended.Grade']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mark3': ('django.db.models.fields.IntegerField', [], {}),
            'mark4': ('django.db.models.fields.IntegerField', [], {}),
            'mark5': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'public': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'share': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['userextended.Teacher']", 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Subject']"}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teacher'", 'to': "orm['userextended.Teacher']"})
        },
        'tests.varianta': {
            'Meta': {'ordering': "['question__number']", 'object_name': 'VariantA'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option1': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'option2': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'option3': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'option4': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tests.Question']"}),
            'task': ('django.db.models.fields.TextField', [], {})
        },
        'tests.variantb': {
            'Meta': {'ordering': "['question__number']", 'object_name': 'VariantB'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tests.Question']"}),
            'task': ('django.db.models.fields.TextField', [], {})
        },
        'userextended.baseuser': {
            'Meta': {'object_name': 'BaseUser'},
            'cart': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'clerk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Clerk']", 'null': 'True', 'blank': 'True'}),
            'current_role': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'userextended_baseuser_related_role_related'", 'null': 'True', 'to': "orm['userextended.BaseUser']"}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'null': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'userextended_baseuser_related_roles_related'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['userextended.BaseUser']"}),
            'sync_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
            'sync_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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

    complete_apps = ['tests']

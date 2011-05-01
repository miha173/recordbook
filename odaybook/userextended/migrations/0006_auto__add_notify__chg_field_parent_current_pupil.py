# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Notify'
        db.create_table('userextended_notify', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.Teacher'], null=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('for_eduadmin', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('for_superviser', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('userextended', ['Notify'])

        # Changing field 'Parent.current_pupil'
        db.alter_column('userextended_parent', 'current_pupil_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['userextended.Pupil']))


    def backwards(self, orm):
        
        # Deleting model 'Notify'
        db.delete_table('userextended_notify')

        # User chose to not deal with backwards NULL issues for 'Parent.current_pupil'
        raise RuntimeError("Cannot reverse this migration. 'Parent.current_pupil' and its values cannot be restored.")


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
        'userextended.achievement': {
            'Meta': {'object_name': 'Achievement'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pupil': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Pupil']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'userextended.baseuser': {
            'Meta': {'object_name': 'BaseUser'},
            'cart': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'clerk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Clerk']", 'null': 'True', 'blank': 'True'}),
            'current_role': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'userextended_baseuser_related_role_related'", 'null': 'True', 'to': "orm['userextended.BaseUser']"}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'null': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'userextended_baseuser_related_roles_related'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['userextended.BaseUser']"}),
            'sync_timestamp': ('django.db.models.fields.IntegerField', [], {}),
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
            'sync_timestamp': ('django.db.models.fields.IntegerField', [], {}),
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
        'userextended.notify': {
            'Meta': {'object_name': 'Notify'},
            'for_eduadmin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'for_superviser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Teacher']", 'null': 'True'})
        },
        'userextended.option': {
            'Meta': {'object_name': 'Option'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.School']", 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'userextended.parent': {
            'Meta': {'object_name': 'Parent', '_ormbases': ['userextended.BaseUser']},
            'baseuser_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['userextended.BaseUser']", 'unique': 'True', 'primary_key': 'True'}),
            'current_pupil': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'userextended_pupil_related'", 'null': 'True', 'to': "orm['userextended.Pupil']"}),
            'pupils': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'userextended_pupils_related'", 'symmetrical': 'False', 'to': "orm['userextended.Pupil']"})
        },
        'userextended.permission': {
            'Meta': {'object_name': 'Permission'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {}),
            'user_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'userextended.pupil': {
            'Meta': {'ordering': "['last_name', 'first_name', 'middle_name']", 'object_name': 'Pupil', '_ormbases': ['userextended.BaseUser']},
            'baseuser_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['userextended.BaseUser']", 'unique': 'True', 'primary_key': 'True'}),
            'grade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Grade']", 'null': 'True'}),
            'health_group': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1', 'null': 'True'}),
            'health_note': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'insurance_policy': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '100', 'null': 'True'}),
            'parent_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parent_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parent_phone_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parent_phone_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.School']", 'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'userextended.pupilconnection': {
            'Meta': {'unique_together': "(('pupil', 'subject'),)", 'object_name': 'PupilConnection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pupil': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Pupil']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.Subject']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
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
        'userextended.staff': {
            'Meta': {'object_name': 'Staff', '_ormbases': ['userextended.BaseUser']},
            'baseuser_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['userextended.BaseUser']", 'unique': 'True', 'primary_key': 'True'}),
            'edu_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.School']", 'null': 'True', 'blank': 'True'}),
            'tech_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'userextended.subject': {
            'Meta': {'ordering': "['name']", 'object_name': 'Subject'},
            'groups': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rest_modified': ('django.db.models.fields.DateTimeField', [], {}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.School']"})
        },
        'userextended.superuser': {
            'Meta': {'object_name': 'Superuser', '_ormbases': ['userextended.BaseUser']},
            'baseuser_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['userextended.BaseUser']", 'unique': 'True', 'primary_key': 'True'})
        },
        'userextended.superviser': {
            'Meta': {'object_name': 'Superviser', '_ormbases': ['userextended.BaseUser']},
            'baseuser_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['userextended.BaseUser']", 'unique': 'True', 'primary_key': 'True'})
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

    complete_apps = ['userextended']

# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'School'
        db.create_table('userextended_school', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rest_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('saturday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('max_mark', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('gapps_use', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gapps_login', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True)),
            ('gapps_password', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True)),
            ('gapps_domain', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True)),
            ('private_domain', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('private_salute', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('userextended', ['School'])

        # Adding model 'Option'
        db.create_table('userextended_option', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.School'], null=True, blank=True)),
        ))
        db.send_create_signal('userextended', ['Option'])

        # Adding model 'Grade'
        db.create_table('userextended_grade', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rest_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('long_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('small_name', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.School'])),
        ))
        db.send_create_signal('userextended', ['Grade'])

        # Adding model 'Subject'
        db.create_table('userextended_subject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rest_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.School'])),
        ))
        db.send_create_signal('userextended', ['Subject'])

        # Adding model 'Clerk'
        db.create_table('userextended_clerk', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('rest_modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('cart', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('current_role', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='userextended_clerk_related_role_related', null=True, to=orm['userextended.BaseUser'])),
            ('sync_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('userextended', ['Clerk'])

        # Adding M2M table for field roles on 'Clerk'
        db.create_table('userextended_clerk_roles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('clerk', models.ForeignKey(orm['userextended.clerk'], null=False)),
            ('baseuser', models.ForeignKey(orm['userextended.baseuser'], null=False))
        ))
        db.create_unique('userextended_clerk_roles', ['clerk_id', 'baseuser_id'])

        # Adding model 'BaseUser'
        db.create_table('userextended_baseuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('cart', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('current_role', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='userextended_baseuser_related_role_related', null=True, to=orm['userextended.BaseUser'])),
            ('sync_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('clerk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.Clerk'], null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=30, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=30, null=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('userextended', ['BaseUser'])

        # Adding M2M table for field roles on 'BaseUser'
        db.create_table('userextended_baseuser_roles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_baseuser', models.ForeignKey(orm['userextended.baseuser'], null=False)),
            ('to_baseuser', models.ForeignKey(orm['userextended.baseuser'], null=False))
        ))
        db.create_unique('userextended_baseuser_roles', ['from_baseuser_id', 'to_baseuser_id'])

        # Adding model 'Teacher'
        db.create_table('userextended_teacher', (
            ('baseuser_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['userextended.BaseUser'], unique=True, primary_key=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.School'], null=True, blank=True)),
            ('edu_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tech_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('grade', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='grade', null=True, to=orm['userextended.Grade'])),
            ('current_subject', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='current_subject', null=True, to=orm['userextended.Subject'])),
            ('current_grade', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='current_grade', null=True, to=orm['userextended.Grade'])),
        ))
        db.send_create_signal('userextended', ['Teacher'])

        # Adding unique constraint on 'Teacher', fields ['grade']
        db.create_unique('userextended_teacher', ['grade_id'])

        # Adding M2M table for field subjects on 'Teacher'
        db.create_table('userextended_teacher_subjects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('teacher', models.ForeignKey(orm['userextended.teacher'], null=False)),
            ('subject', models.ForeignKey(orm['userextended.subject'], null=False))
        ))
        db.create_unique('userextended_teacher_subjects', ['teacher_id', 'subject_id'])

        # Adding M2M table for field grades on 'Teacher'
        db.create_table('userextended_teacher_grades', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('teacher', models.ForeignKey(orm['userextended.teacher'], null=False)),
            ('grade', models.ForeignKey(orm['userextended.grade'], null=False))
        ))
        db.create_unique('userextended_teacher_grades', ['teacher_id', 'grade_id'])

        # Adding model 'Parent'
        db.create_table('userextended_parent', (
            ('baseuser_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['userextended.BaseUser'], unique=True, primary_key=True)),
            ('current_pupil', self.gf('django.db.models.fields.related.ForeignKey')(related_name='userextended_pupil_related', to=orm['userextended.Pupil'])),
        ))
        db.send_create_signal('userextended', ['Parent'])

        # Adding M2M table for field pupils on 'Parent'
        db.create_table('userextended_parent_pupils', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('parent', models.ForeignKey(orm['userextended.parent'], null=False)),
            ('pupil', models.ForeignKey(orm['userextended.pupil'], null=False))
        ))
        db.create_unique('userextended_parent_pupils', ['parent_id', 'pupil_id'])

        # Adding model 'Pupil'
        db.create_table('userextended_pupil', (
            ('baseuser_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['userextended.BaseUser'], unique=True, primary_key=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.School'], null=True, blank=True)),
            ('grade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.Grade'], null=True)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('special', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('health_group', self.gf('django.db.models.fields.CharField')(default='1', max_length=1, null=True)),
            ('health_note', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True)),
            ('order', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('parent_1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('parent_2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('parent_phone_1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('parent_phone_2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('insurance_policy', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('userextended', ['Pupil'])

        # Adding model 'Staff'
        db.create_table('userextended_staff', (
            ('baseuser_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['userextended.BaseUser'], unique=True, primary_key=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.School'], null=True, blank=True)),
            ('edu_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tech_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('userextended', ['Staff'])

        # Adding model 'Superviser'
        db.create_table('userextended_superviser', (
            ('baseuser_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['userextended.BaseUser'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('userextended', ['Superviser'])

        # Adding model 'Superuser'
        db.create_table('userextended_superuser', (
            ('baseuser_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['userextended.BaseUser'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('userextended', ['Superuser'])

        # Adding model 'Achievement'
        db.create_table('userextended_achievement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('pupil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['userextended.Pupil'])),
        ))
        db.send_create_signal('userextended', ['Achievement'])

        # Adding model 'Permission'
        db.create_table('userextended_permission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('user_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('permission', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('userextended', ['Permission'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Teacher', fields ['grade']
        db.delete_unique('userextended_teacher', ['grade_id'])

        # Deleting model 'School'
        db.delete_table('userextended_school')

        # Deleting model 'Option'
        db.delete_table('userextended_option')

        # Deleting model 'Grade'
        db.delete_table('userextended_grade')

        # Deleting model 'Subject'
        db.delete_table('userextended_subject')

        # Deleting model 'Clerk'
        db.delete_table('userextended_clerk')

        # Removing M2M table for field roles on 'Clerk'
        db.delete_table('userextended_clerk_roles')

        # Deleting model 'BaseUser'
        db.delete_table('userextended_baseuser')

        # Removing M2M table for field roles on 'BaseUser'
        db.delete_table('userextended_baseuser_roles')

        # Deleting model 'Teacher'
        db.delete_table('userextended_teacher')

        # Removing M2M table for field subjects on 'Teacher'
        db.delete_table('userextended_teacher_subjects')

        # Removing M2M table for field grades on 'Teacher'
        db.delete_table('userextended_teacher_grades')

        # Deleting model 'Parent'
        db.delete_table('userextended_parent')

        # Removing M2M table for field pupils on 'Parent'
        db.delete_table('userextended_parent_pupils')

        # Deleting model 'Pupil'
        db.delete_table('userextended_pupil')

        # Deleting model 'Staff'
        db.delete_table('userextended_staff')

        # Deleting model 'Superviser'
        db.delete_table('userextended_superviser')

        # Deleting model 'Superuser'
        db.delete_table('userextended_superuser')

        # Deleting model 'Achievement'
        db.delete_table('userextended_achievement')

        # Deleting model 'Permission'
        db.delete_table('userextended_permission')


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
            'current_pupil': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'userextended_pupil_related'", 'to': "orm['userextended.Pupil']"}),
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
        'userextended.staff': {
            'Meta': {'object_name': 'Staff', '_ormbases': ['userextended.BaseUser']},
            'baseuser_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['userextended.BaseUser']", 'unique': 'True', 'primary_key': 'True'}),
            'edu_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['userextended.School']", 'null': 'True', 'blank': 'True'}),
            'tech_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'userextended.subject': {
            'Meta': {'ordering': "['name']", 'object_name': 'Subject'},
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

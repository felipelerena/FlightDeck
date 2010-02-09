
from south.db import db
from django.db import models
from jetpack.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Jetpack'
        db.create_table('jetpack_jetpack', (
            ('id', orm['jetpack.Jetpack:id']),
            ('slug', orm['jetpack.Jetpack:slug']),
            ('name', orm['jetpack.Jetpack:name']),
            ('decription', orm['jetpack.Jetpack:decription']),
            ('author', orm['jetpack.Jetpack:author']),
            ('public_permission', orm['jetpack.Jetpack:public_permission']),
            ('group_permission', orm['jetpack.Jetpack:group_permission']),
        ))
        db.send_create_signal('jetpack', ['Jetpack'])
        
        # Adding model 'Version'
        db.create_table('jetpack_version', (
            ('id', orm['jetpack.Version:id']),
            ('jetpack', orm['jetpack.Version:jetpack']),
            ('name', orm['jetpack.Version:name']),
            ('decription', orm['jetpack.Version:decription']),
            ('code', orm['jetpack.Version:code']),
            ('status', orm['jetpack.Version:status']),
            ('published', orm['jetpack.Version:published']),
            ('is_base', orm['jetpack.Version:is_base']),
        ))
        db.send_create_signal('jetpack', ['Version'])
        
        # Adding ManyToManyField 'Jetpack.managers'
        db.create_table('jetpack_jetpack_managers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('jetpack', models.ForeignKey(orm.Jetpack, null=False)),
            ('user', models.ForeignKey(orm['auth.User'], null=False))
        ))
        
        # Adding ManyToManyField 'Jetpack.developers'
        db.create_table('jetpack_jetpack_developers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('jetpack', models.ForeignKey(orm.Jetpack, null=False)),
            ('user', models.ForeignKey(orm['auth.User'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Jetpack'
        db.delete_table('jetpack_jetpack')
        
        # Deleting model 'Version'
        db.delete_table('jetpack_version')
        
        # Dropping ManyToManyField 'Jetpack.managers'
        db.delete_table('jetpack_jetpack_managers')
        
        # Dropping ManyToManyField 'Jetpack.developers'
        db.delete_table('jetpack_jetpack_developers')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'jetpack.jetpack': {
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'authored_jetpacks'", 'to': "orm['auth.User']"}),
            'decription': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'developers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']"}),
            'group_permission': ('django.db.models.fields.IntegerField', [], {'default': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'public_permission': ('django.db.models.fields.IntegerField', [], {'default': '2', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'jetpack.version': {
            'code': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'decription': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_base': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'jetpack': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'versions'", 'to': "orm['jetpack.Jetpack']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'a'", 'max_length': '1', 'blank': 'True'})
        }
    }
    
    complete_apps = ['jetpack']

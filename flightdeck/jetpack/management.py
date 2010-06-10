import os
import simplejson

from django.db.models import signals
from django.contrib.auth.models import User

from jetpack import models as jetpack_models
from jetpack.models import Package, Module, PackageRevision
from jetpack import settings
from person.models import Profile

def install_jetpack_core(sender, created_models, **kwargs):
	# check if that's the syncdb to create jetpack models
	if not (jetpack_models.Package in created_models and \
			jetpack_models.PackageRevision in created_models):
		return
	
	# check if the jetpack-sdk was already installed
	sdk_dir = '%s/src/jetpack-sdk' % settings.VIRTUAL_ENV
	if not os.path.isdir(sdk_dir):
		raise Exception("Please install jetpack SDK first")

	# create core user
	core_author = User.objects.create(username='mozilla',first_name='Mozilla')
	Profile.objects.create(user=core_author)

	# create Jetpack Core Library
	handle = open('%s/packages/jetpack-core/package.json' % sdk_dir)
	core_manifest = simplejson.loads(handle.read())
	handle.close()
	core_contributors = [core_manifest['author']]
	core_contributors.extend(core_manifest['contributors'])
	core = Package(
		author=core_author, # sorry Atul
		full_name='Jetpack Core',
		name='jetpack-core',
		type='l',
		public_permission=2,
		description=core_manifest['description']
	)
	core.save()
	core_revision = core.latest
	core_revision.set_version(core_manifest['version'])
	core_revision.contributors = ', '.join(core_contributors)
	super(PackageRevision, core_revision).save()
	core_lib_dir = '%s/packages/jetpack-core/lib' % sdk_dir
	core_modules = os.listdir(core_lib_dir)
	for module_file in core_modules:
		module_path = '%s/%s' % (core_lib_dir, module_file)
		module_name = os.path.splitext(module_file)[0]
		handle = open(module_path, 'r')
		module_code = handle.read()
		handle.close()
		mod = Module.objects.create(
			filename=module_name,
			code=module_code,
			author=core_author
		)
		core_revision.modules.add(mod)
	print "Jetpack Core Library created successfully"

signals.post_syncdb.connect(install_jetpack_core, sender=jetpack_models)


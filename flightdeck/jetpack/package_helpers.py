from base.shortcuts import get_object_or_create, get_object_with_related_or_404, get_random_string
from jetpack.models import Package, PackageRevision 

def get_package_revision(id, type, revision_number=None, version_name=None, latest=False):
	"""
	Return revision of the package
	"""
	if not (revision_number or version_name):
		# get default revision - one linked via Package:version
		package = get_object_with_related_or_404(Package, id_number=id, type=type)
		package_revision = package.latest if latest else package.version

	elif revision_number:
		# get version given by revision number
		package_revision = get_object_with_related_or_404(PackageRevision, 
							package__id_number=id, package__type=type,
							revision_number=revision_number)
	elif version_name:
		# get version given by version name
		package_revision = get_object_with_related_or_404(PackageRevision, 
							package__id_number=id, package__type=type,
							version_name=version_name)
	return package_revision



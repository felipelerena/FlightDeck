"""
a set of defs used to manage xpi
"""

import os
import shutil
import subprocess
import stat

from jetpack import settings


def sdk_copy(sdk_dir):
	""" 
	copy the sdk to the sdk_dir
	create cfx.sh which will set environment and call 'real' cfx
	"""
	shutil.copytree('%s/src/jetpack-sdk' % settings.VIRTUAL_ENV, sdk_dir)
	# create cfx.sh
	handle = open('%s/bin/cfx.sh' % sdk_dir, 'w')
	handle.write("""#!/bin/bash
source %s/bin/activate
#CUDDLEFISH_ROOT=%s
#export CUDDLEFISH_ROOT
cfx $*""" % (sdk_dir, sdk_dir))
	handle.close()
	os.chmod('%s/bin/cfx.sh' % sdk_dir, stat.S_IXUSR|stat.S_IRUSR)
	


def xpi_build(sdk_dir, package_dir):
	" build xpi from source in sdk_dir "
	# set environment
	#os.environ['CUDDLEFISH_ROOT'] = sdk_dir
	old_path = os.environ['PATH']
	os.environ['PATH'] = '%s/bin:%s' % (sdk_dir, old_path)

	# create XPI
	os.chdir(package_dir)
	cfx_command = [
		'%s/bin/cfx.sh' % sdk_dir,
		'--binary=/usr/bin/xulrunner',
		'xpi']

	try:
		process = subprocess.Popen(
						cfx_command, 
						shell=False, 
						stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	except subprocess.CalledProcessError:
		return HttpResponseServerError

	out = process.communicate()
	#if out[1] and not settings.DEBUG:
		#xpi_remove(sdk_dir)
	
	# clean up environment
	os.environ['PATH'] = old_path

	# return cfx result
	return out

def xpi_remove(sdk_dir):
	" clear directory "
	shutil.rmtree(sdk_dir)

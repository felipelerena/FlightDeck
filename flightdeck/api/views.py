import os
import sys

from cuddlefish import apiparser

from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse, \
						HttpResponseNotAllowed, HttpResponseServerError
from django.template import RequestContext#,Template
from django.utils import simplejson

from base.shortcuts import get_object_or_create, get_object_with_related_or_404, \
						get_random_string

from api import settings

def _get_module_filenames(package_name):
	files = os.listdir(os.path.join(settings.SDKPACKAGESDIR,package_name,'docs'))
	files.sort()
	return files

def _get_module_names(package_name):
	DOC_FILES = _get_module_filenames(package_name)
	return [{'name': os.path.splitext(d)[0]} for d in DOC_FILES]
	modules.sort()
	return modules


def homepage(r, package_name='jetpack-core'):
	page = 'apibrowser'

	package = {'name': package_name, 'modules': _get_module_names(package_name)}

	return render_to_response(
		'api_homepage.html', 
		locals(),
		context_instance=RequestContext(r))


def package(r, package_name='jetpack-core'):
	"""
	containing a listing of all modules docs
	"""
	page = 'apibrowser'

	DOC_FILES = _get_module_filenames(package_name)

	package = {'name': package_name, 'modules': []}
	for d in DOC_FILES:
		text = open(os.path.join(settings.SDKPACKAGESDIR,package_name,'docs',d)).read()
		(doc_name, extension) = os.path.splitext(d)
		# changing the tuples to dictionaries
		hunks = list(apiparser.parse_hunks(text))
		data = {}
		for h in hunks:
			data[h[0]] = h[1]
		package['modules'].append({
			'name': doc_name,
			'info': hunks[0][1],
			'data': data,
			'hunks': hunks
		})
	
	return render_to_response(
		'package_doc.html', 
		locals(),
		context_instance=RequestContext(r))
		
def module(r, package_name, module_name):
	page = 'apibrowser'
	
	doc_file = '.'.join((module_name,'md'))
	text = open(os.path.join(settings.SDKPACKAGESDIR,package_name,'docs',doc_file)).read()
	# changing the tuples to dictionaries
	hunks = list(apiparser.parse_hunks(text))
	data = []
	for h in hunks:
		# convert JSON to a nice list
		if h[0] == 'api-json':
			entity = h[1]
			entity['template'] = '_entity_%s.html' % entity['type']
			data.append(entity)
		
	module = {
		'name': module_name,
		'info': hunks[0][1],
		'data': data,
		'hunks': hunks
	}
	package = {'name': package_name, 'modules': _get_module_names(package_name)}
	
	return render_to_response(
		'module_doc.html', 
		locals(),
		context_instance=RequestContext(r))

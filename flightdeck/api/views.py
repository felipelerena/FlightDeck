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


def package(r, package_name):
	"""
	containing a listing of all modules docs
	"""

	DOC_FILES = os.listdir(os.path.join(settings.SDKPACKAGESDIR,package_name,'docs'))

	package = {'name': package_name, 'modules': []}
	import pprint
	for d in DOC_FILES:
		text = open(os.path.join(settings.SDKPACKAGESDIR,package_name,'docs',d)).read()
		(doc_name, extension) = os.path.splitext(d)
		# changing the tuples to dictionaries
		hunks = list(apiparser.parse_hunks(text))
		pprint.pprint(hunks)
		print('-------------------------------------')
		data = {}
		for h in hunks:
			data[h[0]] = h[1]
		package['modules'].append({
			'name': doc_name,
			'info': data['markdown'],
			'data': data,
			'hunks': hunks
		})
	
	page = 'api'
	
	return render_to_response(
		'package_doc.html', 
		locals(),
		context_instance=RequestContext(r))
		
def module(r, package_name, module_name):
	doc_file = '.'.join((module_name,'md'))
	text = open(os.path.join(settings.SDKPACKAGESDIR,package_name,'docs',doc_file,'.rd')).read()
	# changing the tuples to dictionaries
	hunks = list(apiparser.parse_hunks(text))
	data = {}
	for h in hunks:
		data[h[0]] = h[1]
	module = {
		'name': doc_name,
		'info': data['markdown'],
		'data': data,
		'hunks': hunks
	}
	
	page = 'api'
	
	return render_to_response(
		'module_doc.html', 
		locals(),
		context_instance=RequestContext(r))

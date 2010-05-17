"""
Testing the cuddlefish engine to export API 
"""

import os
from django.test import TestCase
from cuddlefish import apiparser
from api import settings

class CuddleTest(TestCase):
	def test_basic(self):
		"""
		exporting hunks
		"""
		docs_dir = os.path.join(settings.VIRTUAL_ENV,'src/jetpack-sdk/packages/jetpack-core/docs')
		text = open(os.path.join(docs_dir,'url.md')).read()
		self.failUnless(len(list(apiparser.parse_hunks(text))) > 0)



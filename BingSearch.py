#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import types
from requests.auth import HTTPBasicAuth

class Constants:
	basic_url='https://api.datamarket.azure.com/Bing/Search/'
	websearch_only_url='https://api.datamarket.azure.com/Bing/SearchWeb/'


API_OPTIONS ={
	'websearch': {
		"Adult":{"types":[types.StringType]},
		"Latitude":{"types":[types.FloatType]},
		"Longitude":{"types":[types.FloatType]},
		"Market":{"types":[types.StringType]},
		"Options":{"types":[types.ListType]}
	}
}

class BingWebsearch:
	
	def __init__(self, azurekey, websearch_only=True):
		self.search_url = Constants.websearch_only_url if websearch_only else Constants.basic_url
		self.key = azurekey

	def checkOptions(self, searchname, options):
		for opt, val in options.iteritems():
			try:
				optdesc = API_OPTIONS[searchname][opt]
			except KeyError:
				raise Exception('option "' + opt + '" is not supported in websearch query type.' + 
					'Supported options: ' + repr(API_OPTIONS['websearch'].keys()))

			if type(val) not in optdesc['types']:
				raise Exception('option "' + opt + '" should be one of types '
					+ repr([x.__name__ for x in optdesc.types]) + 'but is type'
					+ type(val).__name__)
			
			if type(val) == types.ListType:
				options[opt] = '+'.join(val)
			
			if type(val) in [types.StringType, types.UnicodeType]:
				options[opt] = u"'" + val + u"'"


	def websearch(self, query, top=None, skip=None, **kwargs):
		if not query:
			raise Exception('empty query')
		self.checkOptions('websearch', kwargs)	
		kwargs.update({
			'Query':u"'" + query + u"'",
			'$format':'json'
			})
		r = requests.get(self.search_url + 'Web', auth=HTTPBasicAuth('', self.key), params=kwargs)
		if r.status_code == requests.codes.ok:
			return r.json()
		else:
			raise Exception(str(r.status_code) + ' url (' + r.url + ') : ' + r.content)


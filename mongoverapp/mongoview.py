from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from pymongo import Connection
import json

@csrf_exempt
def index(request):
	db_list = {}
	c = Connection()
	dbs = c.database_names()
	for db in dbs:
		col = c[db].collection_names()
		sys_index = 'system.indexes'
		if sys_index in col:
			col.remove('system.indexes')
		print col
		db_list.update({db:col})
		print db_list
	return render_to_response('mongoviewer.html', {'dbs':db_list},context_instance=RequestContext(request))

def viewcollection(request):
	if request.method == 'GET':
		db = request.GET.get('db')
		col = request.GET.get('col')
		searchcriteria = request.GET.get('searchcriteria')
		c = Connection()
		data = c[db][col]
		if IsNotNull(searchcriteria):
			full_data = data.find(json.loads(searchcriteria))
		else:
			full_data = data.find({})
		full_data_list = []
		key_list = []
		for d in full_data:
			for key in d:
				if key not in key_list:
					key_list.append(key)
			full_data_list.append(d)
		db_list = load_dbs_collections()
	return render_to_response('collectiondata.html', {'dbs':db_list,'data':full_data_list,'key_list':key_list,'db':db,'col':col},context_instance=RequestContext(request))

def load_dbs_collections():
	db_list = {}
	c = Connection()
	dbs = c.database_names()
	for db in dbs:
		col = c[db].collection_names()
		sys_index = 'system.indexes'
		if sys_index in col:
			col.remove('system.indexes')
		print col
		db_list.update({db:col})
	return db_list

def IsNotNull(value):
    return value is not None and len(value) > 0	
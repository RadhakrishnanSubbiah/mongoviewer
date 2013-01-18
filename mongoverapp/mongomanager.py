from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from pymongo import MongoClient
from bson.objectid import ObjectId
from mongoviewer.settings import CONFIG_LOCATION
from django.http import HttpResponse
import json, ast, re

@csrf_exempt
def delete(request):
	response_data = {}
	if request.method == 'POST':
		_id = request.POST.get('_id')
		db = request.POST.get('db')
		col = request.POST.get('col')
		host = request.POST.get('host')
		port = request.POST.get('port')
		c = MongoClient(host, int(port))
		database = c[db][col]
		print _id
		database.remove({'_id':ObjectId(_id)})
		response_data['status'] = 'Record deleted successfully!'
	return HttpResponse(json.dumps(response_data),  mimetype='application/json')
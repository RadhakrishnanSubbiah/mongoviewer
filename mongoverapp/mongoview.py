from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from pymongo import MongoClient
from mongoviewer.settings import CONFIG_LOCATION
from django.http import HttpResponse
import json, ast, re


@csrf_exempt
def index(request):
	return render_to_response('mongoviewer.html', {'mongoRepoList':GetMongoRepoList()},context_instance=RequestContext(request))

def viewcollection(request):
	if request.method == 'GET':
		db = request.GET.get('db')
		col = request.GET.get('col')
		host = request.GET.get('host')
		port = request.GET.get('port')
		searchcriteria = request.GET.get('searchcriteria')
		c = MongoClient(host, int(port))
		print c[db]
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
			#print ast.literal_eval(json.dumps(d))
			full_data_list.append(d)
		#db_list = load_dbs_collections()
	return render_to_response('collectiondata.html', {'data':full_data_list,'key_list':key_list,'db':db,'col':col},context_instance=RequestContext(request))

def load_database(request):
	if request.method == 'GET':
		profileName = request.GET.get('profilename')
		host = request.GET.get('host')
		port = request.GET.get('port')
		c = MongoClient(host, int(port))
		completeList= {}
		db_list = {}
		c = MongoClient(host,int(port))
		dbs = c.database_names()
		for db in dbs:
			col = c[db].collection_names()
			sys_index = 'system.indexes'
			if sys_index in col:
				col.remove('system.indexes')
			print col
			db_list.update({db:col})
		profileName = profileName + '[' + host + ':' + port + ']'
		completeList.update({profileName:db_list})
	return render_to_response('database.html', {'dbs':completeList},context_instance=RequestContext(request))

@csrf_exempt
def manage_profile(request):
	print 'manage profile method'
	if request.method == 'POST':
		profileName = request.POST.get('mongoconf')
		name = request.POST.get('name')
		host = request.POST.get('server')
		port = request.POST.get('port')
		mode = request.POST.get('mode')
		mongoRepoList = GetMongoRepoList()
		message = ""
		status = "success"
		response_data = {}
		try:
			if mode == "edit":
				for key in mongoRepoList.iterkeys():
					value = mongoRepoList[key]
					if name in value:
						temp = [name, host + ':' + port]
						mongoRepoList.update({key:temp})
						break
				WriteToFile(mongoRepoList)
				message = "Record saved successfully."
			elif mode == "add":
				print "add called"
				profileAlreadyExist = False
				for key in mongoRepoList.iterkeys():
					value = mongoRepoList[key]
					if name in value:
						profileAlreadyExist = True
						break
				if profileAlreadyExist:
					print "coming here"
					message = "Profile name already exists."
					raise Exception("Profile Already Exists")
				temp = [name,host + ':' + port]
				mongoRepoList.update({len(mongoRepoList)+1:temp})
				print mongoRepoList
				WriteToFile(mongoRepoList)
				message = "Record saved successfully."
			else:
				for key in mongoRepoList.iterkeys():
					value = mongoRepoList[key]
					if name in value:
						temp = [name, host + ':' + port]
						del mongoRepoList[key]
						break
				WriteToFile(mongoRepoList)
				message = "Record deleted successfully."
		except Exception, e:
			print 'Error '
			status = "error"
			pass
		response_data['status'] = status
		response_data['message'] = message
		response_data['mongoRepoList'] = mongoRepoList
		print json.dumps(response_data)
	return HttpResponse(json.dumps(response_data),  mimetype='application/json')
	
def IsNotNull(value):
    return value is not None and len(value) > 0	
	
def GetMongoRepoList():
	mongoRepoList = {}
	f = open(CONFIG_LOCATION)
	count = 1
	for line in f:
		splitter = re.compile('\|')
		test = splitter.split(line.rstrip())
		mongoRepoList.update({count:test})
		count = count + 1
	f.close()
	return mongoRepoList

def WriteToFile(mongoRepoList):
	try:
		f = open(CONFIG_LOCATION, 'w')
		f.write("")
		temp = ''
		for key in mongoRepoList.iterkeys():
			value = mongoRepoList[key]
			temp = temp + value[0] + '|' + value[1] + '\n'
		f.write(temp)	
		f.close()
	except:
		raise Exception("Problem in saving the data.")
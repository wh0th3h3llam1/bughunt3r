from django.http import HttpResponse, HttpResponseRedirect
from bughunt3r.settings import STATIC_URL
from django.shortcuts import render
from datetime import datetime
from os.path import isfile, join
from os import listdir, walk
import urllib.request
import requests
import sublist3r
import os, time
import http.client as httplib

# Create your views here.

COLORS = ['red', 'orange', 'yellow', 'olive', 'green', 'teal', 'blue', 'violet', 'purple', 'pink', 'brown', 'grey', 'black']

def home(request):

	files_path = os.getcwd() + "\engine\static\scan_results"
	try:
		x = [f for f in listdir(files_path) if isfile(join(files_path, f))][-1]
		temp = x.split('.')
		ts = temp[0]
		dt = datetime.fromtimestamp(int(temp[0]))
		type = temp[-1]
		domain = ".".join(temp[1:-1])

		res = {'timestamp':ts, 'type': type, 'domain': domain, 'dt': dt}
	except:
		res = None
	
	context = {
		"last_result": res,
		"colors": COLORS,	
	}
	return render(request, 'engine/home.html', context)


def results(request, id=None):
	
	files_path = os.getcwd() + "\engine\static\scan_results"
	try:
		onlyfiles = [f for f in listdir(files_path) if isfile(join(files_path, f))]
	
	except:
		onlyfiles = None

	# Forwarded from Subdomain Enumeration
	if request.method == 'POST':
		cwd = os.getcwd()
		url = request.POST['url']
		tool = request.POST.get('tool')
		timestamp = int(datetime.timestamp(datetime.now()))
		
		file_name = f"\engine\static\scan_results\{timestamp}.{url}.subdomain"
		with open(cwd + file_name, "w+") as f:
			pass
		
		if tool == "sublist3r":
			subdomains = sublist3r.main(url, 40, cwd + file_name, ports=None, silent=False, verbose=False, enable_bruteforce=False, engines=None)
		
		else:
			subdomains = os.system(f'{cwd}\\engine\\templates\\tools\\subfinder\\subfinder.exe ' + f"-d {url} -o {cwd}{file_name} -silent")
			# print(f'{cwd}\\engine\\templates\\tools\\subfinder\\subfinder.exe ' + f"-d {url} -o {cwd}{file_name}")
			# subfinder.exe -d djangoproject.com -o C:\Users\Aarsh\Documents\Programming\CyberSecurity\BISAG\bughunt3r\engine\static\scan_results\1614139948.djangoproject.subdomain -silent
		all_results = get_results(get_files())
		context = {"all_results": all_results[::-1]}

		return render(request, 'engine/results.html', context)
	
	# results/**
	else:

		# results/[id]
		if id is not None:
			data = domain = None
			for i in onlyfiles:
				temp = i.split('.')
				if int(temp[0]) == int(id):
					with open(files_path + "\\" + str(i), "r") as f:
						data = list(map(str, f.read().split()))
						domain = ".".join(temp[1:-1])
			
			status = list()
			for d in data:
				# print('---------------------------------------------')
				# print("Scanning for " + d)
				try:
					conn = httplib.HTTPConnection(d)
					conn.request("HEAD", "/")
					x = conn.getresponse()
					# print(d, end="\t")
					if x:
						# print(x.status, x.reason)
						status.append({'msg': x.reason, 'status': str(x.status)})
					else:
						# print("NO Response from " + d)
						status.append({'msg': 'Not Found', 'status': str(404)})
				except:
					status.append({'msg': 'Not Found', 'status': str(404)})
				finally:
					conn.close()

			# print(status)
			r = zip(data, status)

			context = {
				"result": r, #data,
				"size": len(data),
				"domain": domain,
				"id": id,
				"colors": COLORS,	
				"dt": datetime.fromtimestamp(int(id))
			}

			return render(request, 'engine/show_result.html', context)
		
		# results/
		else:
			# all_results = list()
			# for i in onlyfiles:
			# 	temp = i.split('.')
			# 	ts = int(temp[0])
			# 	dt = datetime.fromtimestamp(int(ts))
			# 	type = temp[-1]
			# 	domain = ".".join(temp[1:-1])
			# 	# print(dt, ts)
			# 	all_results.append({'dt': dt, 'id': ts, 'type': type, 'domain': domain})
			
			all_results = get_results(get_files())
			context = {
				"all_results": all_results[::-1],
				'colors': COLORS
			}

			return render(request, 'engine/results.html', context)


def subdomain(request):
	context = {}
	return render(request, 'engine/subdomain_enum.html', context)


def findSubdomains(request):
	cwd = os.getcwd()
	url = request.POST['url']

	timestamp = int(datetime.timestamp(datetime.now()))
	# print(timestamp)
	# print(datetime.fromtimestamp(timestamp))
	
	file_name = f"\engine\static\scan_results\{timestamp}.{url}.subdomain"
	with open(cwd + file_name, "w+") as f:
		pass
	
	subdomains = sublist3r.main(url, 40, cwd + file_name, ports=None, silent=False, verbose=False, enable_bruteforce=False, engines=None)
	# with open(cwd + file_name, "w+") as f:
	# 	data = list(map(str, f.read().split()))
	
	all_results = get_results(get_files())
	context = {"all_results": all_results[::-1]}

	return render(request, 'engine/results.html', context)


def portscan(request):
	context = {}
	return render(request, 'engine/portscan.html', context)


def about(request):
	return render(request, 'engine/about.html')


def test(request):
	return render(request, 'engine/test.html')


def get_files() -> list:
	files_path = os.getcwd() + "\engine\static\scan_results"
	try:
		onlyfiles = [f for f in listdir(files_path) if isfile(join(files_path, f))]
	except:
		onlyfiles = None

	return onlyfiles


def get_results(only_files) -> list:
	all_results = list()
	for i in only_files:
		temp = i.split('.')
		ts = int(temp[0])
		dt = datetime.fromtimestamp(int(ts))
		type = temp[-1]
		domain = ".".join(temp[1:-1])
		all_results.append({'dt': dt, 'id': ts, 'type': type, 'domain': domain})
	
	return all_results
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from bughunt3r.settings import STATIC_URL
from django.shortcuts import render
from datetime import datetime
from os.path import isfile, join
from os import listdir, walk
from .templates.tools.masscan import masscan

import sublist3r, nmap, masscan
import http.client as httplib
import requests, os, time
import urllib.request
import glob, json

# Create your views here.


COLORS = ['red', 'orange', 'yellow', 'olive', 'green', 'teal', 'blue', 'violet', 'purple', 'pink', 'brown', 'grey']


def home(request):

	files_path = os.getcwd() + "\engine\static\scan_results"
	try:
		x = [f for f in listdir(files_path) if isfile(join(files_path, f))][-1]
		temp = x.split('.')
		ts = temp[0]
		dt = datetime.fromtimestamp(int(temp[0]))
		type = temp[-1]
		tool = temp[-2]
		domain = ".".join(temp[1:-2])

		res = {'timestamp':ts, 'type': type, 'domain': domain, 'dt': dt, 'tool': tool}
	except:
		res = None
	
	context = {
		"last_result": res,
		"colors": COLORS,	
	}
	return render(request, 'engine/home.html', context)


def results(request, type=None, id=None):
	print("In Results")
	files_path = os.getcwd() + "\engine\static\scan_results"
	try:
		onlyfiles = [f for f in listdir(files_path) if isfile(join(files_path, f))]
	
	except:
		onlyfiles = None

	# Forwarded from Subdomain Enumeration or Port Scan
	if request.method == 'POST':
		scan_type = request.POST['scan_type']
		
		# If forwarded from Subdomain Enum
		if scan_type == "subdomain-enum":
			cwd = os.getcwd()
			url = request.POST['url']
			tool = request.POST.get('tool')
			scan_type = 'subdomain-enum'
			timestamp = int(datetime.timestamp(datetime.now()))
			
			file_name = f"\engine\static\scan_results\{timestamp}.{url}.{tool}.{scan_type}"
			f = open(cwd + file_name, "w+")
			# with open(cwd + file_name, "w+") as f:
				# pass
			
			if tool == "sublist3r":
				subdomains = sublist3r.main(url, 40, cwd + file_name, ports=None, silent=False, verbose=False, enable_bruteforce=False, engines=None)
			
			else:
				subdomains = os.system(f'{cwd}\\engine\\templates\\tools\\subfinder\\subfinder.exe ' + f"-d {url} -o {cwd}{file_name} -silent")
			
			all_results = get_results(get_files(type=scan_type))
			context = {
				"all_results": all_results[::-1],
				"scan_type": scan_type,
				'colors': COLORS
			}

			return render(request, 'engine/results_subdomain_enum.html', context)
		
		# If forwarded from Port Scan
		elif scan_type == "port-scan":
			print("scan-type: port-scan")
			domain_ip = request.POST['domain_ip']
			port_range = request.POST['ports']
			tool = request.POST.get('tool')
			print(f'tool: {tool}')
			timestamp = int(datetime.timestamp(datetime.now()))
			
			file_name = f"\engine\static\scan_results\{timestamp}.{domain_ip}.{tool}.{scan_type}"
			
			if tool == "nmap":
				print("nmap scan started")
				nm = nmap.PortScanner()
				res = nm.scan(hosts=domain_ip, ports=port_range)
				print(res)
				with open(os.getcwd() + file_name, "w+") as f:
					f.writelines(res)

			elif tool == "masscan":
				ms = masscan.PortScanner()
				print(ms.scan(domain_ip, ports='22,80,420', arguments='--max-rate 1000').scan_result)
				# print(ms.scan_result)
			elif tool == "rust":
				pass
			else:
				print("Error")
				
			# print(domain_ip)
			# print(ports)

			# all_results = get_results(get_files(type=scan_type))
			all_results = get_results(get_files())
			context = {
				"all_results": all_results[::-1],
				"scan_type": scan_type,
				'colors': COLORS
			}

			# return render(request, 'engine/results_portscan.html', context)
			return render(request, 'engine/results_all.html', context)
		
		else:
			print("ERROR in RESULTS if type - subdomain/port")
	
	# results/**
	else:
		print("In else")
		# results/[type]/[id]
		if id is not None:
			print("id: " + str(id))
			r = data = domain = None
			for i in onlyfiles:
				temp = i.split('.')
				if int(temp[0]) == int(id):
					with open(files_path + "\\" + str(i), "r") as f:
						data = list(map(str, f.read().split()))
						domain = ".".join(temp[1:-1])
			
			active = 0
			# status = list()
			# if data is not None:
			# 	for d in data:
			# 		try:
			# 			conn = httplib.HTTPConnection(d)
			# 			conn.request("HEAD", "/")
			# 			x = conn.getresponse()
			# 			if x:
			# 				status.append({'msg': x.reason, 'status': str(x.status)})
			# 				if str(x.status).startswith('2') or str(x.status).startswith('3'):
			# 					active += 1
			# 			else:
			# 				status.append({'msg': 'Not Found', 'status': str(404)})
			# 		except:
			# 			status.append({'msg': 'Not Found', 'status': str(404)})
			# 		finally:
			# 			conn.close()

			# 	r = zip(data, status)


			context = {
				"result": r if r else data,
				"size": len(data) if data else 0,
				"active": active,
				"domain": domain,
				"id": id,
				"colors": COLORS,	
				"dt": datetime.fromtimestamp(int(id))
			}

			if type == "subdomain-enum":
				return render(request, 'engine/show_result_subdomain_enum.html', context)

			if type == "port-scan":
				
				for i in onlyfiles:
					temp = i.split('.')
					if int(temp[0]) == int(id):
						with open(files_path + "\\" + str(i), "r") as f:
							data = f.read()
				o = ""
				# o = json.loads(data)
				# print(json.dumps(o, indent=4))
				print(data)
				context = {
					"result": o if o else None,
					"id": id,
					"colors": COLORS,	
					"dt": datetime.fromtimestamp(int(id))
				}
				return render(request, 'engine/show_result_portscan.html', context)

			if type == "all":
				return render(request, 'engine/show_result.html', context)

		
		# /results/[type]
		elif type:
			print("In type")
			
			if type == "subdomain-enum":

				all_results = get_results(get_files(type='subdomain-enum'))
				context = {
					"all_results": all_results[::-1],
					"scan_type": type,
					'colors': COLORS
				}

				return render(request, 'engine/results_subdomain_enum.html', context)

			elif type == "port-scan":
				all_results = get_results(get_files(type=type))
				context = {
					"all_results": all_results[::-1],
					"scan_type": type,
					'colors': COLORS
				}

				return render(request, 'engine/results_portscan.html', context)

			elif type == "all":

				all_results = get_results(get_files())
				context = {
					"all_results": all_results[::-1],
					"scan_type": type,
					'colors': COLORS
				}

				return render(request, 'engine/results_all.html', context)

			else:
				return render(request, 'engine/not_found.html')


		# results/
		else:
			# all_results = list()
			# for i in onlyfiles:
			# 	temp = i.split('.')
			# 	ts = int(temp[0])
			# 	dt = datetime.fromtimestamp(int(ts))
			# 	type = temp[-1]
			# 	tool = temp[-2]
			# 	domain = ".".join(temp[1:-2])
			# 	# print(dt, ts)
			# 	all_results.append({'dt': dt, 'id': ts, 'type': type, 'domain': domain})
			
			# all_results = get_results(get_files())
			context = {
				# "all_results": all_results[::-1],
				'colors': COLORS
			}
			print("In else else")
			return render(request, 'engine/results_choice.html', context)


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
	
	if request.method == 'POST':
		domain_ip = request.POST['domain_ip']
		ports = request.POST['ports']
		tool = request.POST.get('tool')
		print(f'tool: {tool}')
		
		if tool == "nmap":
			nm = nmap.PortScanner()
			print(nm.scan(hosts=domain_ip, ports=ports))
		elif tool == "masscan":
			ms = masscan.PortScanner()
			print(ms.scan(domain_ip, ports='22,80,420', arguments='--max-rate 1000').scan_result)
			# print(ms.scan_result)
		elif tool == "rust":
			pass
		else:
			print("Error")
			
		print(domain_ip)
		print(ports)

		return render(request, 'engine/results.html')
	
	context = {}
	return render(request, 'engine/portscan.html', context)


def about(request):
	context = {
		"colors": COLORS
	}
	return render(request, 'engine/about.html', context)


def test(request):
	return render(request, 'engine/test.html')


def get_files(type=None) -> list:

	files_path = os.getcwd() + "\engine\static\scan_results"
	# if type == "port-scan":
	# 	print("type: port-scan")
	# 	x = glob.glob(f"{files_path}\*.{type}")
	# 	print(x)
	# 	return x


	if type:
		print(f"type: {type}")
		# print("glob.glob")
		temp = list()
		x = [f for f in listdir(files_path) if isfile(join(files_path, f))]
		for i in x:
			if i.endswith(type):
				temp.append(i)
		onlyfiles = temp
	else:
		try:
			onlyfiles = [f for f in listdir(files_path) if isfile(join(files_path, f))]
		except:
			onlyfiles = None

	# print("onlyfiles: ")
	# print(onlyfiles)
	return onlyfiles


"""
def get_files(type=None) -> list:

	print("In get_files")
	print("type: " + type)
	files_path = os.getcwd() + "\engine\static\scan_results"
	if type:
		print(f"{files_path}\*.{type}")
		return glob.glob(f"{files_path}\*.{type}")
	else:
		try:
			onlyfiles = [f for f in listdir(files_path) if isfile(join(files_path, f))]
		except:
			onlyfiles = None

	print("onlyfiles: ")
	print(onlyfiles)
	return onlyfiles
"""

def get_results(only_files) -> list:
	all_results = list()
	
	try:
		for i in only_files:
			temp = i.split('.')
			# print(temp)
			ts = int(temp[0])
			dt = datetime.fromtimestamp(int(ts))
			type = temp[-1]
			domain = ".".join(temp[1:-2])
			tool = temp[-2]
			all_results.append({
				'dt': dt,
				'id': ts,
				'type': type,
				'tool': tool,
				'domain': domain
			})
	
	except:
		all_results = []

	return all_results
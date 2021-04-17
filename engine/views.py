from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .templates.tools.masscan import masscan
from django.views.static import serve
from bughunt3r.settings import STATIC_URL, STATIC_ROOT, EYEWITNESS_URL
from django.shortcuts import render
from datetime import datetime
from os.path import isfile, join, isdir, exists
from pathlib import Path
from ipware import get_client_ip
from ares import CVESearch
from os import listdir, walk

import sublist3r, nmap, masscan
import http.client as httplib
import requests, os, time
import logging, traceback
import _pickle as pickle
import hashlib, shutil
import urllib.request
import glob, json
import markdown

# Create your views here.

CWD = os.getcwd()
COLORS = ['red', 'orange', 'yellow', 'olive', 'green', 'teal', 'blue', 'violet', 'purple', 'pink', 'brown', 'grey']

AUTH_CONFIG = "auth\config.json"
AUTH_CONFIG_PATH = f"{CWD}\engine\static\{AUTH_CONFIG}"

SCAN_RESULTS = "\engine\static\scan_results"


def auth():
	if exists(AUTH_CONFIG_PATH):
		print("authentication file exists")
		with open(AUTH_CONFIG_PATH, "r") as f:
			data = f.read()

		if not data:
			print("file empty")
			return False

		else:
			conf = json.loads(data)
			cred = conf['bughunt3r']['config']
			unm = cred['user_name']
			pwd = cred['password']
			if unm == "" or pwd == "":
				return False
			else:
				return True

	else:
		return False


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

		res = {'timestamp': ts, 'type': type, 'domain': domain, 'dt': dt, 'tool': tool}
	except:
		res = None
	
	
	if auth():
		auth_setup = True
	else:
		auth_setup = False
	print(f"auth_setup {auth_setup}")

	scan_all = len(get_results(get_files()))
	scan_subdomain = len(get_results(get_files(type="subdomain-enum")))
	scan_port = len(get_results(get_files(type="port-scan")))

	context = {
		"last_result": res,
		"colors": COLORS,
		"auth_setup": auth_setup,
		"scan_all": scan_all,
		"scan_subdomain": scan_subdomain,
		"scan_port": scan_port,
	}
	return render(request, 'engine/home.html', context)


# def results(request, type=None, id=None, delete=None, active=None):
def results(request, type=None, id=None, action=None, detailed_report=None):
	print("In Results")
	files_path = CWD + SCAN_RESULTS
	try:
		onlyfiles = [f for f in listdir(files_path) if isfile(join(files_path, f))]
	
	except:
		onlyfiles = None

	# Forwarded from Subdomain Enumeration or Port Scan
	if request.method == 'POST':
		scan_type = request.POST['scan_type']
		
		# If forwarded from Subdomain Enum
		if scan_type == "subdomain-enum":
			url = request.POST['url']
			tool = request.POST.get('tool')
			scan_type = 'subdomain-enum'
			timestamp = int(datetime.timestamp(datetime.now()))
			
			file_name = f"{SCAN_RESULTS}\{timestamp}.{url}.{tool}.{scan_type}"
			f = open(CWD + file_name, "w+")
			
			try:
				# sublist3r
				if tool == "sublist3r":
					subdomains = sublist3r.main(url, 40, CWD + file_name, ports=None, silent=False, verbose=False, enable_bruteforce=False, engines=None)
				
				# subfinder
				elif tool == "subfinder":
					subdomains = os.system(f'{CWD}\\engine\\templates\\tools\\subfinder\\subfinder.exe -d {url} -o {CWD}{file_name} -silent')
					
				# assetfinder
				elif tool == "assetfinder":
					subdomains = os.system(f'{CWD}\\engine\\templates\\tools\\assetfinder\\assetfinder.exe -d {url} >> {CWD}{file_name}')

				# amass
				else:
					subdomains = os.system(f'{CWD}\\engine\\templates\\tools\\amass\\amass.exe enum -d {url} -o {CWD}{file_name} -silent')
			
			except Exception as e:
				print("Error Scanning subdommains")
				print(str(e))

			all_results = get_results(get_files(type=scan_type))

			if auth():
				auth_setup = True
			else:
				auth_setup = False
			
			context = {
				"auth_setup": auth_setup,
				"all_results": all_results[::-1],
				"scan_type": scan_type,
				'colors': COLORS
			}

			return render(request, 'engine/results_subdomain_enum.html', context)
		
		# If forwarded from Port Scan
		elif scan_type == "port-scan":
			print("scan-type: port-scan")
			url = request.POST['url']
			port_range = request.POST['ports']
			tool = request.POST.get('tool')
			options = request.POST['options']
			print(f'tool: {tool}')
			timestamp = int(datetime.timestamp(datetime.now()))
			
			file_name = f"{SCAN_RESULTS}\{timestamp}.{url}.{tool}.{scan_type}"
			
			if tool == "nmap":
				print("nmap scan started")
				nm = nmap.PortScanner()
				res = nm.scan(hosts=url, ports=port_range, arguments=options)
				with open(os.getcwd() + file_name, "w") as f:
					f.write(json.dumps(res)) 

			elif tool == "masscan":
				ms = masscan.PortScanner()
				print(ms.scan(url, ports='22,80,420', arguments='--max-rate 1000').scan_result)
				# print(ms.scan_result)
				
			elif tool == "rust":
				pass

			else:
				print("Error")
				return render(request, 'engine/not_found.html')
				
			# all_results = get_results(get_files(type=scan_type))
			all_results = get_results(get_files())

			if auth():
				auth_setup = True
			else:
				auth_setup = False
			
			context = {
				"auth_setup": auth_setup,
				"all_results": all_results[::-1],
				"scan_type": scan_type,
				'colors': COLORS
			}

			# return render(request, 'engine/results_portscan.html', context)
			return render(request, 'engine/results_all.html', context)
		
		else:
			print("ERROR in RESULTS : none of type - subdomain/port-scan")
	
	# results/**
	else:
		print("In else")
		# results/[type]/[id]/[action]
		if id is not None:
			data = None
			print(f"action: {action}")
			print(f"id: {id}")
			
			# results/[type]/[id]/delete
			if action == "delete":
				print("Delete initiated")
				try:
					name = str(glob.glob(f"{files_path}\{id}*{type}")[0]).replace('\\\\', '\\')
					os.remove(name)
					message = "Deleted"
					print("Deleted Succesfully")
				
				except Exception as e:
					print(e)
					print("Error Deleting File")
					message = "Error"
				
				finally:
					all_results = get_results(get_files(type=type))

					if auth():
						auth_setup = True
					else:
						auth_setup = False
					
					context = {
						"auth_setup": auth_setup,
						"all_results": all_results[::-1],
						"message": message,
						"scan_type": type,
						'colors': COLORS
					}

					if type == "subdomain-enum":
						return render(request, 'engine/results_subdomain_enum.html', context)
					
					else:
						return render(request, 'engine/results_portscan.html', context)

			# results/[type]/[id]/eyewitness
			if action == "eyewitness":
				
				print("In eyewitness")
				subdomain_scan_file = Path(glob.glob(f"{files_path}\{id}*{type}")[0]).absolute()
				try:
					os.system(f'{CWD}\\engine\\templates\\tools\\eyewitness\\EyeWitness.exe -f {subdomain_scan_file}')
					eyewitness_path = f"{EYEWITNESS_URL}\\EyeWitness_"
					ew = glob.glob(f"{eyewitness_path}*")[-1]

					# images = list()
					final = list()
					for (_, _, filenames) in walk(f"{ew}\\images"):
						# images.extend(filenames)
						for f in filenames:
							final.append(f"{ew}\\images\\{f}")

					
					img = f"{CWD}\\engine\\images"
					if exists(img):
						print("removing images")
						shutil.rmtree(img)
						
					print("creating images folder")
					os.makedirs(img)

					print("copying images ")
					for f in final:
						print("copying image: " + f)
						shutil.copy2(f, img)

					print("*****************************************************************************")
					print(f"CWD: {CWD}")
					print("*****************************************************************************")
					if detailed_report == "detailed_report":
						file = glob.glob(f"{ew}\\report*")[0]
						return serve(request, os.path.basename(file), os.path.dirname(file))
					
					local_images = glob.glob(f"{img}\*")
					# print(local_images)
					# li = []
					# for i in local_images:
					# 	li.append("images" + i)
					# print(final)

					if auth():
						auth_setup = True
					else:
						auth_setup = False
					
					context = {
						"auth_setup": auth_setup,
						"images": local_images,
						"id": id,
						"colors": COLORS,	
					}

					return render(request, 'engine/eyewitness.html', context)

				except Exception as e:
					print("Error in eyewitness")
					print(e)
			
			# results/[type]/[id]/eyewitness
			if action == "cve-search":
				cve = CVESearch()
				print('cveInfo')
				# z = cve.browse('microsoft/')
				z = cve.browse('cpe:/o:microsoft:windows')
				print(z)

				return HttpResponse(f"{z}")
			# print("id: " + str(id))
			tool_used = None

			# results/[type]/[id]
			if type == "subdomain-enum":
				r = domain = None
				# print(f"type: {type}")
				
				# Read File
				for i in onlyfiles:
					temp = i.split('.')
					if int(temp[0]) == int(id):
						with open(files_path + "\\" + str(i), "r") as f:
							data = list(map(str, f.read().split()))
							domain = ".".join(temp[1:-2])
							tool_used = temp[-2]
				
				if data:
					# print(f"data: {data}")
					active_domains = 0
					status = list()
					# print(f"active: {action}")
					if action == "active":
						active = action
						print("in active")
						
						if data is not None:
							for d in data:
								print(d)
								try:
									conn = httplib.HTTPConnection(d)
									conn.request("HEAD", "/")
									x = conn.getresponse()
									if x:
										status.append({'msg': x.reason, 'status': str(x.status)})
										if str(x.status).startswith('2') or str(x.status).startswith('3'):
											active_domains += 1
									else:
										status.append({'msg': 'Not Found', 'status': str(404)})
								except:
									status.append({'msg': 'Not Found', 'status': str(404)})
								finally:
									conn.close()

							r = zip(data, status)
					
					else:
						active = None
						r = data
					

					if auth():
						auth_setup = True
					else:
						auth_setup = False
					
					context = {
						"auth_setup": auth_setup,
						"result": r if r else data,
						"size": len(data) if data else 0,
						"active": active,
						"active_domains": active_domains,
						"domain": domain,
						"tool_used": tool_used,
						"id": id,
						"colors": COLORS,	
						"dt": datetime.fromtimestamp(int(id))
					}
				
				else:

					if auth():
						auth_setup = True
					else:
						auth_setup = False
					
					context = {
						"auth_setup": auth_setup,
						"result": "empty",
						"id": id,
						"tool": tool_used,
						"colors": COLORS,
						# "dt": datetime.fromtimestamp(int(id))
					}

				return render(request, 'engine/show_result_subdomain_enum.html', context)

			if type == "port-scan":
				output = None
				hostname = domain = None
				cmd = t = port_range = scan_info = os_detection_info = os_class = None
				for i in onlyfiles:
					temp = i.split('.')
					if int(temp[0]) == int(id):
						with open(files_path + "\\" + str(i), "r") as f:
							data = f.read()
							domain = ".".join(temp[1:-2])
							tool_used = temp[-2]
							
				if data:
					output = json.loads(data)
					# print(f"domain: {domain}")
					try:
						scan_info = output['scan'][domain]
						hostname = scan_info['hostnames'][0]['name']
					except:
						pass
						# scan_info = None
						
					try:
						os_info = output['scan'][domain]['osmatch'][0]
						os_name = os_info['name']
						accuracy = os_info['accuracy']
						os_detection_info = {
							"os_name": os_name,
							"accuracy": accuracy,
						}
						os_class = output['scan'][domain]['osmatch'][0]['osclass']

					except:
						pass
						# os_detection_info = None
						# os_class = None
					try:
						cmd = output['nmap']['command_line']
						t = cmd.index("-p")
						port_range = cmd[t + 3:].split()[0]
					except:
						pass


				if auth():
					auth_setup = True
				else:
					auth_setup = False

				context = {
					"auth_setup": auth_setup,
					"result": output,# if output else None,
					"scan_info": scan_info,
					"hostname": hostname,
					"os_info": os_detection_info,
					"os_class": os_class,
					"port_range": port_range,
					"id": id,
					"domain": domain,
					"tool_used": tool_used,
					"colors": COLORS,	
					"dt": datetime.fromtimestamp(int(id))
				}
				return render(request, 'engine/show_result_portscan.html', context)

		# /results/[type]
		elif type:
			print("In type")
			
			if type == "subdomain-enum":

				all_results = get_results(get_files(type='subdomain-enum'))

				if auth():
					auth_setup = True
				else:
					auth_setup = False
				
				context = {
					"auth_setup": auth_setup,
					"all_results": all_results[::-1],
					"scan_type": type,
					'colors': COLORS
				}

				return render(request, 'engine/results_subdomain_enum.html', context)

			elif type == "port-scan":
				all_results = get_results(get_files(type=type))

				if auth():
					auth_setup = True
				else:
					auth_setup = False
				
				context = {
					"auth_setup": auth_setup,
					"all_results": all_results[::-1],
					"scan_type": type,
					'colors': COLORS
				}

				return render(request, 'engine/results_portscan.html', context)

			elif type == "all":

				all_results = get_results(get_files())

				if auth():
					auth_setup = True
				else:
					auth_setup = False
				
				context = {
					"auth_setup": auth_setup,
					"all_results": all_results[::-1],
					"scan_type": type,
					'colors': COLORS
				}

				return render(request, 'engine/results_all.html', context)

			else:
				return render(request, 'engine/not_found.html')


		# results/
		else:
			scan_all = len(get_results(get_files()))
			scan_subdomain = len(get_results(get_files(type="subdomain-enum")))
			scan_port = len(get_results(get_files(type="port-scan")))


			if auth():
				auth_setup = True
			else:
				auth_setup = False

			context = {
				"auth_setup": auth_setup,
				"colors": COLORS,
				"scan_all": scan_all,
				"scan_subdomain": scan_subdomain,
				"scan_port": scan_port,
			}
			print("In else else")
			return render(request, 'engine/results_choice.html', context)


def subdomain(request):

	if auth():
		auth_setup = True
	else:
		auth_setup = False
	
	context = {
		"auth_setup": auth_setup,
	}
	return render(request, 'engine/subdomain_enum.html', context)


def portscan(request):
	
	if request.method == 'POST':
		url = request.POST['url']
		ports = request.POST['ports']
		tool = request.POST.get('tool')
		print(f'tool: {tool}')
		
		if tool == "nmap":
			nm = nmap.PortScanner()
			print(nm.scan(hosts=url, ports=ports))
		elif tool == "masscan":
			ms = masscan.PortScanner()
			print(ms.scan(url, ports='22,80,420', arguments='--max-rate 1000').scan_result)
			# print(ms.scan_result)
		elif tool == "rust":
			pass
		else:
			print("Error")
			
		print(url)
		print(ports)

		return render(request, 'engine/results.html')
	

	if auth():
		auth_setup = True
	else:
		auth_setup = False
	
	context = {
		"auth_setup": auth_setup,
	}
	return render(request, 'engine/portscan.html', context)


def about(request):
	ip_add = request.META.get("REMOTE_ADDR")

	client_ip, is_routable = get_client_ip(request)
	if client_ip is None:
		# Unable to get the client's IP address
		print("Cant Get IP")
	else:
		# We got the client's IP address
		if is_routable:
			# The client's IP address is publicly routable on the Internet
			print(client_ip)
		else:
			# The client's IP address is private
			print("The client's IP address is private")
			print(client_ip)
			

	# Order of precedence is (Public, Private, Loopback, None)

	if auth():
		auth_setup = True
	else:
		auth_setup = False
	
	context = {
		"auth_setup": auth_setup,
		"colors": COLORS,
		"ip_add": ip_add
	}
	return render(request, 'engine/about.html', context)


def detailed_report(request, type=None, id=None, eyewitness=None, detailed_report=None,):
	try:
		eyewitness_path = f"{EYEWITNESS_URL}\\EyeWitness_"
		ew = glob.glob(f"{eyewitness_path}*")[-1]
		file = glob.glob(f"{ew}\\report*")[0]
		return serve(request, os.path.basename(file), os.path.dirname(file))
		# context = {
		# 	"images": final,
		# 	"id": id,
		# 	"colors": COLORS,	
		# }

		# return render(request, 'engine/eyewitness.html', context)

	except Exception as e:
		print("Error")
		print(e)


def export_scan_results(request, scan_type=None, tool=None, id=None):
	filepath = f"{CWD}{SCAN_RESULTS}\{id}*{tool}*{scan_type}"
	try:
		file = glob.glob(filepath)[0]
		return serve(request, os.path.basename(file), os.path.dirname(file))
	
	except:
		print("Error Finding File")
		return HttpResponse("Error Finding File")


def raw_file(request, scan_type=None, tool=None, id=None):
	filepath = f"{CWD}{SCAN_RESULTS}\{id}*{tool}*{scan_type}"
	try:
		file = glob.glob(filepath)[0]
		if scan_type == "subdomain-enum":
			data = open(file, "r").read().replace("\n", "<br>")
		else:
			data = open(file, "r").read().replace("\n", "<br>")
		return HttpResponse(data)
	except Exception as e:
		print("Error Finding File")
		print(e)
		return HttpResponse("Error Finding File")


def settings(request, delete=None, type=None):

	if delete:
		files_path = CWD + SCAN_RESULTS
		try:
			onlyfiles = [f for f in listdir(files_path) if isfile(join(files_path, f))]
		except:
			onlyfiles = None
		
		if type == "subdomain-enum" or type == "port-scan":
			all_results = get_results(get_files(type=type))
		
		elif type == "all":
			all_results = get_results(get_files())
		
		else:
			print("Invalid type")


	if request.method == 'POST':
		user_name = request.POST['user_name']
		password = request.POST['passwd']
		algorithm = request.POST.get('algo')
		recovery_email = request.POST['recovery']
		
		print(user_name)
		print(password)
		print(algorithm)
		encoded_pwd = password.encode()
		# print(hashlib.sha256(password.encode()).hexdigest())

		if algorithm == "sha256":
			encrypted_pwd = hashlib.sha256(encoded_pwd).hexdigest()
			print(f"sha256_encoded: {encrypted_pwd}")

		elif algorithm == "sha512":
			encrypted_pwd = hashlib.sha512(encoded_pwd).hexdigest()
			print(f"sha512_encoded: {encrypted_pwd}")

		elif algorithm == "sha3_256":
			encrypted_pwd = hashlib.sha3_256(encoded_pwd).hexdigest()
			print(f"sha3_256_encoded: {encrypted_pwd}")

		elif algorithm == "sha3_512":
			encrypted_pwd = hashlib.sha3_512(encoded_pwd).hexdigest()
			print(f"sha3_512_encoded: {encrypted_pwd}")
		
		else:
			encrypted_pwd = hashlib.md5(encoded_pwd).hexdigest()
			print(f"md5_encoded: {encrypted_pwd}")
		
		print(recovery_email)
		now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


		with open(AUTH_CONFIG_PATH, "r") as f:
			data = f.read()

		config_info = {
			"bughunt3r": {
				"config": {
					"user_name": f"{user_name}",
					"password": f"{encrypted_pwd}",
					"algorithm": f"{algorithm}",
					"recovery_email": f"{recovery_email}",
					"created_on": f"{now}",
					"updated_on": f"{now}"
				}
			}
		}
		# print(config_info)
		# conf = json.loads(data)
		# cred = conf['bughunt3r']['config']
		# cred['user_name'] = f"{user_name}"
		# cred['password'] = f"{encrypted_pwd}"
		# cred['algorithm'] = f"{algorithm}"
		# cred['recovery_email'] = f"{recovery_email}"
		# cred['created_on'] = f"{now}"
		# cred['updated_on'] = f"{now}"

		print('---------------------------------------------------')
		print(config_info)
		try:
			with open(AUTH_CONFIG_PATH, "w") as f:
				f.write(json.dumps(config_info))
		except Exception as e:
			print(str(e))
			return HttpResponse("Couldn't write to config file")

		context = {
			"": ""
		}

		return render(request, 'engine/home.html', context)
	auth_setup = False
	credentials = None

	if auth():
		auth_setup = True
		
		with open(AUTH_CONFIG_PATH, "r") as f:
			data = f.read()

		if not data:
			print("file empty")
			return False
		else:
			conf = json.loads(data)
			cred = conf['bughunt3r']['config']
			unm = cred['user_name']
			pwd = cred['password']

			credentials = {
				'usernm': unm,
				'passwd': pwd
			}
		
	print(f"auth_setup {auth_setup}")

	context = {
		"colors" : COLORS,
		"auth_setup": auth_setup,
		"credentials": credentials,
	}
	return render(request, 'engine/settings.html', context)


def readme(request):
	with open(CWD + "\README.md", "r") as f:
		data = f.read()
	
	md = markdown.Markdown()
	data = md.convert(data)
	print(f"data: {data}")

	context = {
		"data" : data,
		"colors": COLORS
	}
	return render(request, 'engine/show_readme.html', context)


def not_found(request):
	
	if auth():
		auth_setup = True
	else:
		auth_setup = False

	context = {
		"auth_setup": auth_setup,
		"colors": COLORS,
	}
	return render(request, 'engine/not_found.html')


def get_files(type=None) -> list:

	files_path = CWD + SCAN_RESULTS
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


def test(request):
	return render(request, 'engine/test.html')
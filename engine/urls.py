from django.conf.urls.static import static
from django.conf.urls import url, include
from django.urls import path, re_path
from django.conf import settings
from . import views

urlpatterns = [

	url(r'^home/$', views.home, name='home'),
	url(r'^subdomain-enum/$', views.subdomain, name='subdomain-enum'),
	url(r'^port-scan/$', views.portscan, name='port-scan'),
	url(r'^settings/$', views.settings, name='settings'),
	url(r'^readme/$', views.readme, name='readme'),
	

	path('results/<str:type>/<int:id>/<str:action>/<detailed_report>', views.results, name='results'),
	path('results/<subdomain-enum>/<int:id>/<active>', views.results, name='results'),

	path('results/<str:type>/<int:id>/<str:action>', views.results, name='results'),
	path('results/<str:type>/<int:id>/<delete>', views.results, name='results'),
	path('results/<str:type>/<int:id>/', views.results, name='results'),
	path('results/<str:type>/', views.results, name='results'),
	# path('results/<int:id>/', views.results, name='results'),
	
	url(r'^results/$', views.results, name='results'),

	url(r'^find-subdomains/$', views.findSubdomains, name='find-subdomains'),

	url(r'^about/$', views.about, name='about'),
	
	url(r'^test/$', views.test, name='test'),

	path('export_scan_results/<str:scan_type>/<str:tool>/<int:id>', views.export_scan_results, name='export_scan_results'),
	path('raw_file/<str:scan_type>/<str:tool>/<int:id>', views.raw_file, name='raw_file'),

	# path('results/<str:type>/<int:id>/<delete>', views.results, name='results'),
	# path('results/<str:type>/<int:id>/<active>', views.results, name='results'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

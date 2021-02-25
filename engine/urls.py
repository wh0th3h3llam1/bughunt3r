from django.conf.urls.static import static
from django.conf.urls import url, include
from django.urls import path, re_path
from django.conf import settings
from . import views

urlpatterns = [

	url(r'^home/$', views.home, name='home'),
	url(r'^subdomain-enum/$', views.subdomain, name='subdomain-enum'),
	url(r'^port-scan/$', views.portscan, name='port-scan'),
	
	path('results/<int:id>/', views.results, name='results'),
	url(r'^results/$', views.results, name='results'),

	url(r'^find-subdomains/$', views.findSubdomains, name='find-subdomains'),

	url(r'^about/$', views.about, name='about'),
	
	url(r'^test/$', views.test, name='test'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
			(r'^$','webapp.views.main_page'),)

from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
	url(r'^mongoviewer/', 'mongoviewer.mongoverapp.mongoview.index'),
	url(r'^viewcollection/$', 'mongoviewer.mongoverapp.mongoview.viewcollection')
)

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url('^(?P<title>\d+)/(?P<section>\d+)/(?P<psection>.+)?$', 
        'laws.views.show_law', name='laws_show_law')
)

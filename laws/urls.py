from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url('^(?P<title>\w+)/(?P<section>\w+)/(?P<psection>.+)?$', 
        'laws.views.show_law', name='laws_show_law')
)

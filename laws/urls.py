from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url('^target/(?P<target>.+)/$', 'laws.views.target', name='laws_target'),
    url('^(?P<title>\w+)/(?P<section>\w+)/$',
        'laws.views.section', name='laws_section'),
)

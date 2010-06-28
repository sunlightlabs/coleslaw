from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url('^target/(?P<target>.+)/$', 'laws.views.target', name='laws_target'),
    url('^(?P<title>\w+)/(?P<section>[-0-9a-zA-Z_,]+)/(?P<psection>\w+)?$', 'laws.views.section', name='laws_section'),
    url('^(?P<title>\w+)/?$', 'laws.views.title_index', name='laws_title_index'),
    url('^/?$', 'laws.views.index', name='laws_index'),
)

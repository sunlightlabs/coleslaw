from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^laws/', include('laws.urls')),
    (r'^admin/', include(admin.site.urls)),
)

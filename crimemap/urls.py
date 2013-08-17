from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.gis import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from apps.map.models import *

from tastypie.api import Api
from apps.map.api import IncidentResource

v1_api = Api(api_name='v1')
v1_api.register(IncidentResource())

admin.autodiscover()

urlpatterns = patterns('',
    # Simple login for securing site on Heroku
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),

    # Admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', admin.site.urls),

    # Project URLs go here
    (r'^api/', include(v1_api.urls)),
    url(r'^map/', 'apps.map.views.map', name = 'map')

)

urlpatterns += staticfiles_urlpatterns()

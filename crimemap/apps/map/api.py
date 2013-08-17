from tastypie.contrib.gis.resources import ModelResource  # Using GeoDjango ModelResource
from django.http import HttpResponse
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from apps.map.models import *
from tastypie.cache import SimpleCache
from tastypie import fields
from django.utils import simplejson as json

class IncidentResource(ModelResource):
	class Meta: 
		queryset = Incident.objects.filter(location__point_location__isnull = False)
		resource_name = 'incident'
		allowed_methods = ['get']
		max_limit = None
		filtering = {
            'type': ALL,
        }

	def dehydrate(self, bundle):
		#bundle dis shit a GEOJSON object, muthafucka! I have no idea what I'm doing!
		bundle.data['geometry'] = json.loads(bundle.obj.location.point_location.geojson)
		bundle.data['type'] = 'Feature'
		bundle.data['properties'] = {
			'crime': bundle.obj.crime.name,
			'disposition' : bundle.obj.disposition.name,

		}
		return bundle


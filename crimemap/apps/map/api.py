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
		type = 'FeatureCollection'
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
			#'date_occured' : bundle.obj.date_occured

		}
		return bundle

class HexResource(ModelResource):
	class Meta:
		queryset = Hexbin.objects.all()
		resource_name = 'hexbin'
		allowed_methods = ['get']
		excludes = ['poly', 'total_count']
		max_limit = None
		filtering = {
			'type': ALL,
			'id': ALL
		}

	def dehydrate(self, bundle):
		bundle.data['type'] = 'Feature'
		bundle.data['geometry'] = json.loads(bundle.obj.poly.json)
		bundle.data['properties'] = {
		'count': bundle.obj.total_count,
		'incidents': bundle.obj.build_violent_stats()
		}
		
		return bundle
		


            		

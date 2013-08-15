from django.contrib.gis import admin

from apps.map.models import *

class LocationAdmin(admin.ModelAdmin):
	list_display = ['name']
	pass

class IncidentAdmin(admin.ModelAdmin):
	pass

admin.site.register(Incident, IncidentAdmin)
admin.site.register(Location, admin.OSMGeoAdmin)
from django.contrib.gis import admin

from apps.map.models import *

class LocationAdmin(admin.OSMGeoAdmin):
	list_display = ['name', 'verified', 'point_location']
	pass

class LocationTypeAdmin(admin.ModelAdmin):
	pass

class IncidentAdmin(admin.ModelAdmin):
	list_display = ['code', 'date_reported', 'crime', 'location']
	pass

admin.site.register(Incident, IncidentAdmin)
#admin.site.register(Location, admin.OSMGeoAdmin)
admin.site.register(LocationType, LocationTypeAdmin)
admin.site.register(Location, LocationAdmin)
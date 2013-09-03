from django.contrib.gis import admin

from apps.map.models import *

class LocationAdmin(admin.OSMGeoAdmin):
	list_display = ['name', 'verified', 'point_location', 'total_count']
	default_lat = 4881940.078889836
	default_lon = -9821718.67269053
	default_zoom = 12

class CrimeAdmin(admin.ModelAdmin):
	list_display = ['name', 'violent']

class LocationTypeAdmin(admin.ModelAdmin):
	pass


class IncidentAdmin(admin.ModelAdmin):
	list_display = ['code', 'date_reported', 'crime', 'location']
	pass

class HexAdmin(admin.OSMGeoAdmin):
	list_display = [id, 'total_count']
	pass
admin.site.register(Incident, IncidentAdmin)
admin.site.register(Hexbin, HexAdmin)
admin.site.register(Crime, CrimeAdmin)
#admin.site.register(Location, admin.OSMGeoAdmin)
admin.site.register(LocationType, LocationTypeAdmin)
admin.site.register(Location, LocationAdmin)
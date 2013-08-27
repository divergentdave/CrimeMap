from django.contrib.gis.db import models
from django.contrib.gis import geos
from django.contrib.gis.gdal import OGRGeometry, OGRGeomType
from django import forms
# Create your models here.

class LocationType(models.Model):
	name = models.CharField(max_length = 255)
	def __unicode__(self):
		return self.name

#class Hexmap(models.Model):
#	geom = models.MultiPolygonField(srid=4326)
#	objects = models.GeoManager()

class Hexbin(models.Model):
	poly = models.MultiPolygonField('IT IS A FUCKING HEXAGON', null=True, geography=True)
	objects = models.GeoManager()

	#def build_stats(self):

class Location(models.Model):
	name = models.CharField(max_length=255)
	address = models.CharField(max_length=255, blank=True)
	location_type = models.ForeignKey(LocationType, blank = True, null = True)
	point_location = models.PointField('GeoDjango point field of this location', null=True, geography=True, blank = True)
	verified = models.BooleanField(blank = True)
	hexbin = models.ForeignKey(Hexbin, blank = True, null = True)

	class Meta:
		ordering = ['name']
  	objects = models.GeoManager()
	
	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.hexbin = self.get_bin()
		super(Location, self).save(*args, **kwargs)

	def get_bin(self):
		hexerbin = None
		if self.point_location:
			# find the hexbin to which this fucker belongs.
			hexes = Hexbin.objects.filter(poly__covers=self.point_location)
			if hexes.count() > 0:
				hexerbin = hexes[0]
			return hexerbin

class Crime(models.Model):
	name = models.CharField(max_length=50)
	def __unicode__(self):
		return self.name

class Disposition(models.Model):
	name = models.CharField(max_length=50)
	def __unicode__(self):
		return self.name

class Incident(models.Model):
	code = models.CharField(max_length = 20)
	location = models.ForeignKey(Location)
	crime = models.ForeignKey(Crime)
	disposition = models.ForeignKey(Disposition)
	date_reported = models.DateField(null = True)
	date_occurred = models.DateField(null = True)
	time_reported = models.TimeField(null = True)
	time_occurred = models.TimeField(null = True)
	def __unicode__(self):
		return self.code
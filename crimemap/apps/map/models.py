from django.contrib.gis.db import models
from django.contrib.gis import geos
from django.contrib.gis.gdal import OGRGeometry, OGRGeomType
from django import forms
# Create your models here.

class Location(models.Model):
	name = models.CharField(max_length=255)
	address = models.CharField(max_length=255, blank=True)
	point_location = models.PointField('GeoDjango point field of this location', null=True, geography=True, blank = True)
	verified = models.BooleanField(blank = True)
	class Meta:
		ordering = ['name']
  	objects = models.GeoManager()
	def __unicode__(self):
		return self.name

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
	time_occurred = models.TimeField(null = True)





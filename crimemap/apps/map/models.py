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
	total_count = models.IntegerField(default = 0, null = True)
	def save_stats(self):
		self.total_count = Incident.objects.filter(location__hexbin = self).count()

	def save(self, **kwargs):
		self.save_stats()
		super(self.__class__, self).save(**kwargs)

	class Meta:
		ordering = ['-total_count']

	def get_incidents(self, month=None, crime= None, violent = None):
		kwargs = {'location__hexbin': self}
		if month: 
			kwargs['date_occurred__month'] = month
		if crime:
			kwargs['crime'] = crime
		if violent:
			kwargs['crime__violent'] = True
		incidents = Incident.objects.filter(**kwargs)
		return incidents

	def build_violent_stats(self):
		incidents = {}

		incident_list = self.get_incidents()

		for incident in incident_list:
			
			code = incident.code
			
			incidents[code] = []

			location = incident.location.name
			crime = incident.crime.name
			disposition = incident.disposition.name
			date = incident.date_occurred
			time = incident.time_occurred

			incidents[code].append({
				'code': code,
				'location': location,
				'crime': crime,
				'date': date,
				'time': time
				})

		return incidents

class Location(models.Model):
	name = models.CharField(max_length=255)
	address = models.CharField(max_length=255, blank=True)
	location_type = models.ForeignKey(LocationType, blank = True, null = True)
	point_location = models.PointField('GeoDjango point field of this location', null=True, geography=True, blank = True)
	verified = models.BooleanField(blank = True)
	hexbin = models.ForeignKey(Hexbin, blank = True, null = True)
	total_count = models.IntegerField(default = 0, null = True)

	def save_stats(self):
		print self.name
		count = Incident.objects.filter(location = self).count()
		print count
		if count > 0:
			self.total_count = count

	class Meta:
		ordering = ['name']
  	objects = models.GeoManager()
	
	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.hexbin = self.get_bin()
		self.save_stats()
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
	total_count = models.IntegerField(default = 0, null = True)
	violent = models.NullBooleanField()
	alcohol = models.NullBooleanField()
	def save_stats(self):
		print self.name
		self.total_count = Incident.objects.filter(crime = self).count()
		return 

	def save(self, **kwargs):
		self.save_stats()
		super(self.__class__, self).save(**kwargs)

	class Meta:
		ordering = ['-total_count']
	def __unicode__(self):
		return self.name

class Disposition(models.Model):
	name = models.CharField(max_length=50)
	total_count = models.IntegerField(default = 0, null = True)

	def save_stats(self):
		print self.name
		self.total_count = Incident.objects.filter(disposition = self).count()

	def save(self, **kwargs):
		self.save_stats()
		super(self.__class__, self).save(**kwargs)

	class Meta:
		ordering = ['-total_count']

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
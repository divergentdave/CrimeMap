import csv
import os
import re

from time import strptime, strftime
from string import split
import datetime
from django.core.management.base import BaseCommand
from apps.map.models import *
from settings.common import SITE_ROOT

class Command(BaseCommand):
	def handle(self, *args, **options):
		working_dir = os.path.join(SITE_ROOT, '../data')
		file_path = os.path.join(working_dir, 'import1.csv')

		handle = csv.reader(open(file_path, 'rU'), delimiter=',', quotechar='"')
		handle.next()

		for index, h in enumerate(handle):
			location_import, location_created = Location.objects.get_or_create(
				name = h[5].strip()
				)
			crime_import, crime_created = Crime.objects.get_or_create(
				name = h[6].strip()
				)
			disposition_import, disposition_created = Disposition.objects.get_or_create(
				name = h[7].strip()
				)

			date_reported_object = strptime(h[1].strip(), '%m/%d/%Y')
			time_reported_object = strptime(h[2].strip(), '%H:%M:00 %p')
			date_occurred_object = strptime(h[3].strip(), '%m/%d/%Y')
			if len(h[4].strip()) > 0:
				time_occurred_object = strptime(h[4].strip(), '%H:%M:00 %p')
			else:
				time_occurred = strptime('', '')



			incident_import, incident_created = Incident.objects.get_or_create(
				code = h[0].strip(),
				date_reported = strftime('%Y-%m-%d', date_reported_object),
				time_reported = strftime('%H:%M', time_reported_object),
				date_occurred = strftime('%Y-%m-%d', date_occurred_object),
				time_occurred = strftime('%H:%M', time_occurred_object),
				crime = crime_import,
				location = location_import,
				disposition = disposition_import
				)

import os
from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from apps.map.models import *
from settings.common import SITE_ROOT

class Command(BaseCommand):
	help = 'I do not know how to make this work well but I am doing it, okay?'
	
	def handle(self, *args, **options):
		self.stdout.write('Using default shapefile location. I guess. I do not really know \n')
		working_dir = os.path.join(SITE_ROOT, '../data')
		hex_shp = os.path.join(working_dir, 'aug25binned.shp')

		hexmap_mapping = {
        'poly': 'MULTIPOLYGON',
		}

		lm = LayerMapping(
                Hexbin,
                hex_shp,
                hexmap_mapping,
            )
		lm.save(verbose = True, progress = True)

		


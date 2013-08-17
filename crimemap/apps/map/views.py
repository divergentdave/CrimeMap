# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from apps.map.models import *
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404


def map(request):
	return render_to_response('mapONE.html')
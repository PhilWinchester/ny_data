import json
import logging

from django.shortcuts import render
from django.http import JsonResponse

from .models import Stations
from .serializers import StationSerializer

# Create your views here.
# NOTE start with functional views b/c we have simple logic and only a few endpoints
# TODO refactor into classes when we start to have more functionality

logger = logging.getLogger(__name__)


def get_stations(request):
    stations = Stations.objects.all()
    stations_data = StationSerializer(stations, many=True)

    return JsonResponse(stations_data.data, safe=False)

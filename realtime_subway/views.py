import json
import logging

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q

from .models import Stations
from .serializers import StationSerializer

# Create your views here.
# NOTE start with functional views b/c we have simple logic and only a few endpoints
# TODO refactor into classes when we start to have more functionality

logger = logging.getLogger(__name__)


def get_all_stations(request):
    stations = Stations.objects.all()
    stations_data = StationSerializer(stations, many=True)

    return JsonResponse(stations_data.data, safe=False)


def get_stations_by_lookup(request):
    lookup_params = {
        'borough': 'station_borough__icontains',
        'lines': 'station_lines__icontains',
    }

    req_params = request.GET.dict()
    
    filter_vals = {
        lookup_params[param]: req_params[param] 
        for param in req_params if param in lookup_params
    }

    stations = Stations.objects.filter(**filter_vals)
    stations_data = StationSerializer(stations, many=True)

    return JsonResponse(stations_data.data, safe=False)


def get_stations_on_route(request, line: str):
    stations = Stations.objects.filter(station_lines__icontains=line)
    stations_data = StationSerializer(stations.all(), many=True)

    return JsonResponse(stations_data.data, safe=False)
    

def get_stations_in_borough(request, borough: str):
    stations = Stations.objects.filter(station_borough__icontains=borough)
    stations_data = StationSerializer(stations.all(), many=True)

    return JsonResponse(stations_data.data, safe=False)

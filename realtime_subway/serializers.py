from rest_framework import serializers

from .models import Stations


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stations

        fields = [
            'mta_id',
            'station_name',
            'station_lines',
            'station_borough',
            'station_elevated',
            'northbound_desc',
            'southbound_desc',
        ]

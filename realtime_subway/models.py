import uuid

from django.db import models
from django.db.models.fields import AutoField, BigAutoField, CharField, DateTimeField, BooleanField, UUIDField


class TrainStatus(models.TextChoices):
    not_started = 1
    in_transit = 2
    finished = 3


# Create your models here.
class Stations(models.Model):
    station_id = AutoField(primary_key=True)
    mta_id = CharField(max_length=4)
    station_name = CharField(max_length=2048)
    station_parent_id = CharField(max_length=3)
    station_latitude = CharField(max_length=10)
    station_longitude = CharField(max_length=10)
    station_lines = CharField(max_length=64)
    station_borough = CharField(max_length=32)
    station_elevated = BooleanField()
    northbound_desc = CharField(max_length=2048)
    southbound_desc = CharField(max_length=2048)
    datetime_created = DateTimeField(auto_now_add=True)
    datetime_updated = DateTimeField(auto_now=True)


class Trains(models.Model):
    event_id = BigAutoField(primary_key=True)
    record_id = CharField(max_length=32)
    train_status = CharField(choices=TrainStatus.choices, max_length=32)
    train_direction = CharField(max_length=5, default='north')
    train_id = CharField(max_length=6)
    train_route = CharField(max_length=2)
    route_start = DateTimeField()
    stop_id= CharField(max_length=6)
    current_stop = models.ForeignKey(Stations, on_delete=models.PROTECT, related_name='current_station')
    next_stop = models.ForeignKey(Stations, on_delete=models.PROTECT, related_name='next_station', null=True)
    estimated_time = CharField(max_length=64)
    historic_time = CharField(max_length=64)
    datetime_created = DateTimeField(auto_now_add=True)
    datetime_updated = DateTimeField(auto_now=True)
    import_id = UUIDField(default=uuid.uuid4)

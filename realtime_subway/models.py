import uuid

from django.db import models
from django.db.models.fields import AutoField, BigAutoField, CharField, DateTimeField, BooleanField, IntegerField, UUIDField


class TrainStatus(models.TextChoices):
    not_started = 1
    in_transit = 2
    finished = 3


class FareType(models.TextChoices):
    """
    Full fare titles are in scripts/fare_data.py
    """
    full_fare = 1
    senior_disabled = 2
    ada_unlimited_7_day = 3
    ada_unlimited_30_day = 4
    joint_rr_tkt = 5
    unlimited_7_day = 6
    unlimited_30_day = 7
    express_bus_7_day = 8
    transit_check = 9
    reduced_fair_2_trip = 10
    rail_road_unlimited = 11
    tcmc_annual = 12
    ezpay_express = 13
    ezpay_unlimited = 14
    path_2_trip = 15
    airtrain_full_fare = 16
    airtrain_30_day = 17
    airtrain_10_trip = 18
    airtrain_monthly = 19
    student = 20
    nice_2_trip = 21
    cuny_120_day = 22
    cuny_60_day = 23
    full_fare_value = 24
    full_fare_7_day = 25
    full_fare_30_day = 26


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
    # TODO figure out better way to use Enum
    train_status = CharField(choices=TrainStatus.choices, max_length=32)
    train_direction = CharField(max_length=5, default='north')
    train_id = CharField(max_length=12)
    train_route = CharField(max_length=2)
    route_start = DateTimeField()
    stop_id = CharField(max_length=6)
    # Making this nullable for now. Torn b/w filtering these out or keeping them to see if they're useful later
    current_stop = models.ForeignKey(Stations, on_delete=models.PROTECT, related_name='current_station', null=True)
    next_stop = models.ForeignKey(Stations, on_delete=models.PROTECT, related_name='next_station', null=True)
    # TODO: stops_left = IntegerField()
    estimated_time = DateTimeField(null=True)
    historic_time = CharField(max_length=64)
    datetime_created = DateTimeField(auto_now_add=True)
    datetime_updated = DateTimeField(auto_now=True)
    import_id = UUIDField(default=uuid.uuid4)


class Fares(models.Model):
    event_id = BigAutoField(primary_key=True)
    datetime_fare_started = DateTimeField()
    datetime_fare_ended = DateTimeField()
    datetime_uploaded = DateTimeField()
    datetime_imported = DateTimeField(auto_now=True)
    # TODO: Figure out Enum Field once all field type variations are found
    # fare_swipe_type = CharField(choices=FareType.choices, max_length=32)
    fare_swipe_type = CharField(max_length=1024)
    station_remote_id = CharField(max_length=4)
    station_name = CharField(max_length=2048)
    swipes = IntegerField()

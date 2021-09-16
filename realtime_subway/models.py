from django.db import models
from django.db.models.fields import AutoField, CharField, DateTimeField, BooleanField

# Create your models here.
class Stations(models.Model):
    station_id = CharField(max_length=4)
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


# class SubwayTimes(models.Model):
    # question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)
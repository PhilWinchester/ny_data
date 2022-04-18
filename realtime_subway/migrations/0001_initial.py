# Generated by Django 4.0.2 on 2022-02-08 19:07

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fares',
            fields=[
                ('event_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('datetime_fare_started', models.DateTimeField()),
                ('datetime_fare_ended', models.DateTimeField()),
                ('datetime_uploaded', models.DateTimeField()),
                ('datetime_imported', models.DateTimeField(auto_now=True)),
                ('fare_swipe_type', models.CharField(max_length=1024)),
                ('station_remote_id', models.CharField(max_length=4)),
                ('station_name', models.CharField(max_length=2048)),
                ('swipes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Stations',
            fields=[
                ('station_id', models.AutoField(primary_key=True, serialize=False)),
                ('mta_id', models.CharField(max_length=4)),
                ('station_name', models.CharField(max_length=2048)),
                ('station_parent_id', models.CharField(max_length=3)),
                ('station_latitude', models.CharField(max_length=10)),
                ('station_longitude', models.CharField(max_length=10)),
                ('station_lines', models.CharField(max_length=64)),
                ('station_borough', models.CharField(max_length=32)),
                ('station_elevated', models.BooleanField()),
                ('northbound_desc', models.CharField(max_length=2048)),
                ('southbound_desc', models.CharField(max_length=2048)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trains',
            fields=[
                ('event_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('record_id', models.CharField(max_length=32)),
                ('train_status', models.CharField(choices=[('1', 'Not Started'), ('2', 'In Transit'), ('3', 'Finished')], max_length=32)),
                ('train_direction', models.CharField(default='north', max_length=5)),
                ('train_id', models.CharField(max_length=12)),
                ('train_route', models.CharField(max_length=2)),
                ('route_start', models.DateTimeField()),
                ('stop_id', models.CharField(max_length=6)),
                ('estimated_time', models.DateTimeField(null=True)),
                ('historic_time', models.CharField(max_length=64)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
                ('import_id', models.UUIDField(default=uuid.uuid4)),
                ('current_stop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='current_station', to='realtime_subway.stations')),
                ('next_stop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='next_station', to='realtime_subway.stations')),
            ],
        ),
    ]

# Generated by Django 3.2.9 on 2021-11-24 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtime_subway', '0002_alter_trains_train_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trains',
            name='estimated_time',
            field=models.DateTimeField(),
        ),
    ]
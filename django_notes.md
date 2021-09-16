# Django Notes

A series of notes/commands I used to get this Django app up.

https://github.com/neoterix/nyc-mta-arrival-notify/blob/master/mta_notification.py
https://github.com/blahblahblah-/goodservice-v2/tree/main/app/models
https://github.com/MobilityData/gtfs-realtime-bindings/tree/master/python


### Initialization 

Create the project:

`django-admin startproject ny_data .`

Create the app:

`python manage.py startapp realtime_subway`

- Add `'realtime_subway.apps.RealtimeSubwayConfig'` to INSTALLED_APPS in the project settings.py.
- Add PSQL config to settings.py

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
```

### Configuring the DB

FROM INSIDE THE WEB CONTAINER

`python manage.py makemigrations realtime_subway`

Inspect a migration file and see the SQL that is going to be run

`python manage.py sqlmigrate realtime_subway 0001`

Run the migration file(s)

`python manage.py migrate`

Connect to an interactive python environment for the django project.

`python manage.py shell`

This lets you import code from anywhere in your django project

```py
from realtime_subway.models import Choice, Question
Question.objects.all()
```


### Working with Django Admin

Create a superuser (ie admin) who can use Djangos admin toolset. Follow the prompts.

`python manage.py createsuperuser`

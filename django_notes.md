# Django Notes

A series of notes/commands I used to get this Django app up. 


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

- `python manage.py` talk to the Django CLI
- `makemigrations` Tell django we want to make a new migration file
- `polls` the application where Django should look for changes in the models files.

`python manage.py makemigrations polls`

Inspect a migration file and see the SQL that is going to be run

- `python manage.py` talk to the Django CLI
- `sqlmigrate` tell Django CLI to run a migration
- `polls` the application django is going to migrate
- `0001` the migration file django is going to inspect

`python manage.py sqlmigrate polls 0001`

Run the migration file(s)

`python manage.py migrate`

Connect to an interactive python environment for the django project.

`python manage.py shell`

This lets you import code from anywhere in your django project

```py
from polls.models import Choice, Question
Question.objects.all()
```


### Working with Django Admin

Create a superuser (ie admin) who can use Djangos admin toolset. Follow the prompts.

`python manage.py createsuperuser`

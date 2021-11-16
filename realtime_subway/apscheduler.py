from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import register_events


from django.conf import settings

from .scripts.ace_data import ace_data

# Create scheduler to run in a thread inside the application process
scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)

def start():
    # Adding this job here instead of to crons.
    # This will do the following:
    # - Add a scheduled job to the job store on application initialization
    # - The job will execute a model class method at midnight each day
    # - replace_existing in combination with the unique ID prevents duplicate copies of the job
    scheduler.add_job(
        ace_data,
        trigger=CronTrigger(second='*/30'),
        id='ace_data',
        max_instances=1,
        replace_existing=True,
    )

    # Add the scheduled jobs to the Django admin interface
    register_events(scheduler)

    scheduler.start()

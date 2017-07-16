from __future__ import absolute_import
from celery.task.base import periodic_task
from celery.schedules import crontab
from eims.utils import check_internal


@periodic_task(run_every=crontab(minute='*/1'))
def check_internal_calibrations_status():
    check_internal()











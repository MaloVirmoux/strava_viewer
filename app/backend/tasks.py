import time

from celery import Celery
from confs import Conf

CONF = Conf()
celery = Celery(
    "tasks",
    broker=CONF.REDIS["broker_url"],
    backend=CONF.REDIS["result_backend_url"],
)


@celery.task
def some_task():
    time.sleep(60)
    return True

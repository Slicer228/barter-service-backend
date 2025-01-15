from src.tasks.celery_cfg import celery
from time import sleep


@celery.task
def send_offer_notification():
    ...

from src.service.tasks.celery_cfg import celery


@celery.task
def send_offer_notification():
    ...

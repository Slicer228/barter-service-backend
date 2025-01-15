from celery import Celery
from config import settings


celery = Celery(
    'tasks',
    broker="redis://"+settings.redis_host,
    include=["src.tasks.tasks"]
)

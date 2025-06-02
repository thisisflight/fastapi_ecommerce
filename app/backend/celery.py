from dataclasses import asdict, dataclass

from celery import Celery

from app.backend import settings


@dataclass(frozen=True)
class CelerySettings:
    task_serializer: str = "json"
    result_serializer: str = "json"
    accept_content: tuple = ("json",)
    timezone: str = "UTC"
    enable_utc: bool = True
    broker_connection_retry_on_startup: bool = True
    task_track_started: bool = True
    result_expires: int = 3600


celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(**asdict(CelerySettings()))


celery_app.autodiscover_tasks(
    packages=["app.workers.tasks"],
    related_name="tasks",
)

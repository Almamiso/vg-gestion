from celery import Celery
import os

broker_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
app = Celery("vg", broker=broker_url, backend=broker_url, include=["app.workers.tasks"])

app.conf.timezone = "UTC"
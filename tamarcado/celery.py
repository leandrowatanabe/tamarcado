from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tamarcado.settings.dev')

app = Celery('tamarcado', broker='redis://localhost:6379/0')

app.autodiscover_tasks()

@app.task
def soma(a,b):
    return a + b
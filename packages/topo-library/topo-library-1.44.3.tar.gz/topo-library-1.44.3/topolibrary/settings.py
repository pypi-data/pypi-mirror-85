from __future__ import absolute_import, unicode_literals
from mongoengine import connect
from mongoengine.connection import disconnect
import os
from celery import Celery


class MongoSettings():
    def __init__(self, db_name=None, host=None, port=None):
        self.mongo_user = os.environ.get("MONGO_USER")
        self.mongo_pass = os.environ.get("MONGO_PASS")
        self.mongo_port = port if port is not None else os.environ.get("MONGO_PORT", 27017)
        self.mongo_host = host if host is not None else os.environ.get("MONGO_HOST","host.docker.internal")
        self.mongo_db = db_name if db_name is not None else os.environ.get("MONGO_DB", "topograph_db")
        self.host = f"mongodb://{self.mongo_host}:{self.mongo_port}"

    def connect(self):
        self.client = connect(self.mongo_db, host=self.host, port=self.mongo_port, connect=False)
        return self.client

    def save(self, document):
        document.save()

    def close(self):
        disconnect()

class CelerySettings():
    def __init__(self, broker_url=None, temp_celery_folder=None, proj_name=None):
        self.celery_broker = broker_url if broker_url is not None else os.environ.get("REDIS_URL", "redis://redis:6379/1")
        self.temp_folder = temp_celery_folder if temp_celery_folder is not None else os.environ.get("TEMP_CELERY_FOLDER", "/tmp/celery-linter")
        self.proj_name = proj_name if proj_name is not None else os.environ.get("CELERY_PROJECT_NAME", "topo_celery_proj")
        self.app = Celery(self.proj_name, broker=self.celery_broker, backend=self.celery_broker)

    def get_app(self):
        return self.app

    def get_temp_folder(self):
        return self.temp_folder

    def add_autodiscover(self, task_name):
        self.app.autodiscover_tasks([
            task_name
        ], force=True)

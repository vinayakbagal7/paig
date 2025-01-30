import logging
import os

from celery import Celery
from kombu import Queue


path = "./.data/broker"
os.makedirs(path, exist_ok=True)

# paths = ["./.data/broker/in", "./.data/broker/out", "./.data/broker/processed"]
# for path in paths:
#     os.makedirs(path, exist_ok=True)


# Initialize Celery
celery_app = Celery(
    "celery_tasks_consumer_service",
    # broker="filesystem://", # File system as a message broker
    broker="redis://localhost:6379/0",  # Redis as a message broker
    # backend="redis://localhost:6379/1"  # Redis as a results backend
    # backend="sqlite+aiosqlite:///db/database.db"  # sqlite as a results backend
    backend="db+sqlite:///db/database.db"  # sqlite as a results backend
    # backend="db+sqlite:///results.sqlite"  # sqlite as a results backend
)

# Optional: Configure additional Celery options
# celery_app.conf.update(
#     task_routes={"myapp.tasks.*": {"queue": "my_queue"}},
#     task_serializer="json",
#     accept_content=["json"],
#     result_serializer="json",
# )

# Logging configuration
celery_app.conf.update(
    broker_transport_options={
        "data_folder_in": path,  # Folder to store incoming messages
        "data_folder_out": path,  # Folder to store outgoing messages
        "data_folder_processed": path,  # Folder for processed messages
    },
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Add a log file configuration
    # worker_log_format='[%(asctime)s: %(levelname)s] %(message)s',
    # worker_task_log_format='[%(asctime)s: %(levelname)s] Task %(task_name)s[%(task_id)s] %(message)s',
    # task_routes={
    #     "queue1.task.*": {"queue": "queue1"},
    #     "queue2.task.*": {"queue": "queue2"},
    # },
    # task_queues = [
    #     Queue("queue1"),
    #     Queue("queue2"),
    # ]
)

# Set up custom logging to a file
logger = logging.getLogger('celery')
handler = logging.FileHandler('celery.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Import task modules to register tasks
import celery_app_pk.tasks
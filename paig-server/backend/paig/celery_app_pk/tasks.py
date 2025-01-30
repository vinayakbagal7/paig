import json

from celery_app_pk.celery_app_st import celery_app


@celery_app.task
def send_email(to_email: str, subject: str, body: str):
    # Simulate sending an email
    print(f"Sending email to {to_email}: {subject}")
    return f"Email sent to {to_email}"


@celery_app.task(name="celery_tasks_consumer_service.tasks.add", queue="queue1")
def add(x, y):
    print(f"Adding {x} + {y}")
    return x + y


@celery_app.task(name="celery_tasks_consumer_service.tasks.division", queue="queue2")
def division(x, y):
    print(f"dividing x={x} by y={y}")
    return x / y


class CustomTaskException(Exception):
    def __init__(self, message, payload=None):
        super().__init__(message)
        self.payload = payload or {}

    def __str__(self):
        return json.dumps({"message": str(self.args[0]), "payload": self.payload})


@celery_app.task(bind=True)
def process_data(self, data):
    # Update task state during execution
    self.update_state(
        state="PROGRESS",
        meta={"progress": "50%", "details": "Data is being processed"}
    )

    # Simulate processing
    processed_data = {"original": data, "processed": [d.upper() for d in data]}
    return {"status": "success", "processed_data": processed_data}


@celery_app.task(bind=True, max_retries=3)
def fragile_task(self, arg):
    try:
        # Simulate a failure
        raise ValueError("Something went wrong!")
    # except ValueError as exc:
    except Exception as exc:
        # Attach custom data to the failure
        # custom_data = {"arg": arg, "details": "This is custom JSON for failure"}
        # raise CustomTaskException("Task failed!", payload=custom_data) from exc
        raise self.retry(exc=exc, countdown=1)




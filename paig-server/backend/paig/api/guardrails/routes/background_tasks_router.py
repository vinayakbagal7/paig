from fastapi import APIRouter

from celery_app_pk.celery_app_st import celery_app
from celery_app_pk.tasks import send_email, division, process_data, fragile_task
from celery.result import AsyncResult

bg_tasks_router = APIRouter()


@bg_tasks_router.post("/send-email/")
async def send_notification(email: str, subject: str, body: str):
    # Call the Celery task asynchronously
    task = send_email.delay(email, subject, body)
    return {"task_id": task.id, "message": "Task submitted"}


@bg_tasks_router.get("/enqueue/")
def enqueue_task(a: int, b: int):
    task = division.delay(a, b)
    return {"task_id": task.id, "status": "Task enqueued"}


@bg_tasks_router.get("/process-data/")
def process_data_task():
    result = process_data.delay(["foo", "bar", "baz"])
    # print(f"Final result: {result.get(timeout=10)}")
    return {"task_id": result.id, "status": "Processing data"}


@bg_tasks_router.get("/fragile-task/")
def fragile_task_task():
    result = fragile_task.delay([42])
    # print(f"Final result: {result.get(timeout=10)}")
    return {"task_id": result.id, "status": "Processing data"}


@bg_tasks_router.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result,
    }


@bg_tasks_router.post("/retry-task/{task_id}")
def retry_task(task_id):
    result = celery_app.AsyncResult(task_id)
    if result.failed():
        result.retry()

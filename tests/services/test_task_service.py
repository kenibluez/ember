from app.core.schemas.task import TaskCreate
from app.core.models.task import TaskStatus

def test_create_task(task_service):
    data = TaskCreate(title="Write tests")
    task = task_service.create(data)

    assert task.id is not None
    assert task.title == "Write tests"
    assert task.status == TaskStatus.TODO

def test_mark_as_completed(task_service):
    data = TaskCreate(title="Finish feature")
    task = task_service.create(data)

    updated = task_service.mark_as(task.id, TaskStatus.COMPLETED)
    assert updated.status == TaskStatus.COMPLETED

from datetime import datetime

from django.test import TestCase
from tasks.models import Task, TaskType, Worker, Position


class ModelTest(TestCase):
    def test_position(self):
        position = Position.objects.create(name="Test")
        self.assertEqual(
            str(position),
            position.name,
        )

    def test_task_type(self):
        task_type = TaskType.objects.create(name="Test")
        self.assertEqual(
            str(task_type),
            task_type.name,
        )

    def test_worker(self):
        position = Position.objects.create(name="Test")
        worker = Worker.objects.create(
            username="Test",
            password="test123",
            first_name="test first",
            last_name="test last",
            position=position,
        )
        self.assertEqual(
            str(worker),
            f"{worker.username}: {worker.first_name} {worker.last_name}",
        )

    def test_get_absolute_url_worker(self):
        position = Position.objects.create(name="Test")
        worker = Worker.objects.create(
            username="Test",
            password="test123",
            first_name="test first",
            last_name="test last",
            position=position,
        )
        self.assertEqual(worker.get_absolute_url(), f"/workers/{worker.id}/")

    def test_task(self):
        task = Task.objects.create(
            name="Test",
            description="Test description",
            deadline=datetime.now(),
            is_completed=False,
            priority="URGENT",
            task_type=TaskType.objects.create(name="Test"),
        )
        worker = Worker.objects.create(
            username="Test",
            password="test123",
            first_name="test first",
            last_name="test last",
            position=Position.objects.create(name="Test"),
        )
        task.assignees.set([worker])
        self.assertEqual(str(task), f"{task.name}: {task.priority}")

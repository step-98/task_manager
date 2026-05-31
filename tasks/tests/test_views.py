from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.models import TaskType, Position, Task, Worker

TASK_TYPE_URL = reverse("tasks:task-type-list")
POSITION_URL = reverse("tasks:position-list")
WORKER_URL = reverse("tasks:worker-list")
TASK_URL = reverse("tasks:task-list")

class PublicTests(TestCase):
    def test_login_required_task_type(self):
        response = self.client.get(TASK_TYPE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_position(self):
        response = self.client.get(POSITION_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_worker(self):
        response = self.client.get(WORKER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_task(self):
        response = self.client.get(TASK_URL)
        self.assertNotEqual(response.status_code, 200)

class PrivateTaskTypeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)
        TaskType.objects.create(name="Bug")
        TaskType.objects.create(name="QA")

    def test_retrieve_tak_type(self):
        response = self.client.get(TASK_TYPE_URL)
        self.assertEqual(response.status_code, 200)
        task_types = TaskType.objects.all()
        self.assertEqual(list(response.context["task_type_list"]), list(task_types))
        self.assertTemplateUsed(response, "tasks/task_type_list.html")

    def test_search_task_type(self):
        response = self.client.get(TASK_TYPE_URL, {"name": "Bug"})
        self.assertContains(response, "Bug")
        self.assertNotContains(response, "QA")


class PrivatePositionTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)
        Position.objects.create(name="Developer")
        Position.objects.create(name="QA")

    def test_retrieve_position(self):
        response = self.client.get(POSITION_URL)
        self.assertEqual(response.status_code, 200)
        positions = Position.objects.all()
        self.assertEqual(list(response.context["position_list"]), list(positions))
        self.assertTemplateUsed(response, "tasks/position_list.html")

    def test_search_position(self):
        response = self.client.get(POSITION_URL, {"name": "Developer"})
        self.assertContains(response, "Developer")
        self.assertNotContains(response, "QA")


class PrivateWorkerTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(
            username="test_worker",
            password="test123",
            first_name="test first",
            last_name="test_last",
            position=self.position
        )
        self.client.force_login(self.worker)

    def test_create_worker(self):
        form_data = {
            "username": "user",
            "password1": "test123user",
            "password2": "test123user",
            "first_name": "User first",
            "last_name": "User last",
            "position": self.position.id
        }
        self.client.post(reverse("tasks:worker-create"), data=form_data)
        new_worker = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(new_worker.first_name, "User first")
        self.assertEqual(new_worker.last_name, "User last")

    def test_search_worker(self):
        bob = get_user_model().objects.create_user(
            username="Bob",
            password="test123",
            position=Position.objects.create(name="Designer")
        )
        paul = get_user_model().objects.create_user(
            username="Paul",
            password="test123",
            position=Position.objects.create(name="QA")
        )
        response = self.client.get(WORKER_URL, {"name": "Bob"})
        self.assertEqual(response.status_code, 200)
        workers = response.context["worker_list"]
        self.assertIn(bob, workers)
        self.assertNotIn(paul, workers)


class PrivateTaskTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(
            username="test_worker",
            password="test123",
            first_name="test first",
            last_name="test_last",
            position=self.position
        )
        self.client.force_login(self.worker)
        self.task_type = TaskType.objects.create(name="Bug")

    def test_retrieve_task(self):
        task1 = Task.objects.create(
            name="Fix navbar",
            deadline="2026-06-21",
            task_type=self.task_type
        )
        task1.assignees.add(self.worker)
        task2 = Task.objects.create(
            name="Fix pagination",
            deadline="2026-06-25",
            task_type=self.task_type
        )
        task2.assignees.add(self.worker)
        response = self.client.get(TASK_URL)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all()
        self.assertEqual(list(response.context["task_list"]), list(tasks))
        self.assertTemplateUsed(response, "tasks/task_list.html")

    def test_search_task(self):
        Task.objects.create(
            name="Fix navbar",
            deadline="2026-06-21",
            task_type=self.task_type
        )
        Task.objects.create(
            name="Fix pagination",
            deadline="2026-06-25",
            task_type=self.task_type
        )
        response = self.client.get(TASK_URL, data={"name": "navbar"})
        self.assertContains(response, "navbar")
        self.assertNotContains(response, "pagination")

    def test_toggle_assign_to_task(self):
        task = Task.objects.create(
            name="Fix navbar",
            deadline="2026-06-21",
            task_type=self.task_type
        )
        url = reverse("tasks:toggle-assign-to-task", args=[task.id])
        self.client.post(url)
        self.assertTrue(task.assignees.filter(id=self.worker.id).exists())
        self.client.post(url)
        self.assertFalse(task.assignees.filter(id=self.worker.id).exists())

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from tasks.models import Position


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test123"
        )
        self.client.force_login(self.admin_user)
        position = Position.objects.create(name="Test")
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="test123",
            position=position
        )

    def test_worker_position_listed(self):
        url = reverse("admin:tasks_worker_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.worker.position)

    def test_worker_detail_position_listed(self):
        url = reverse("admin:tasks_worker_change", args=[self.worker.id])
        response = self.client.get(url)
        self.assertContains(response, self.worker.position)

    def test_worker_add_position_listed(self):
        url = reverse("admin:tasks_worker_add")
        response = self.client.get(url)
        self.assertContains(response, "position")

from django.test import TestCase

from tasks.forms import (
    WorkerCreationForm,
    PositionSearchForm,
    TaskTypeSearchForm,
    WorkerSearchForm,
    TaskSearchForm,
)
from tasks.models import Position


class FormsTests(TestCase):
    def test_worker_creation_form(self):
        form_data = {
            "username": "user",
            "password1": "test123user",
            "password2": "test123user",
            "first_name": "User first",
            "last_name": "User last",
            "position": Position.objects.create(name="Test"),
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])
        self.assertEqual(form.cleaned_data["position"], form_data["position"])

    def test_position_search_form_empty(self):
        form = PositionSearchForm()
        self.assertEqual(form.fields["name"].label, "")

    def test_position_search_form_not_required(self):
        form = PositionSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_position_search_form(self):
        form = PositionSearchForm(data={"name": "Test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Test")

    def test_task_type_search_form_empty(self):
        form = TaskTypeSearchForm()
        self.assertEqual(form.fields["name"].label, "")

    def test_task_type_search_form_not_required(self):
        form = TaskTypeSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_task_type_search_form(self):
        form = TaskTypeSearchForm(data={"name": "Test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Test")

    def test_worker_search_form_empty(self):
        form = WorkerSearchForm()
        self.assertEqual(form.fields["name"].label, "")

    def test_worker_search_form_not_required(self):
        form = WorkerSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_worker_search_form(self):
        form = WorkerSearchForm(data={"name": "Test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Test")

    def test_task_search_form_empty(self):
        form = TaskSearchForm()
        self.assertEqual(form.fields["name"].label, "")

    def test_task_search_form_not_required(self):
        form = TaskSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_task_search_form(self):
        form = TaskSearchForm(data={"name": "Test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Test")

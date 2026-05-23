from django.urls import path, include
from tasks.views import index, TaskTypeListView, WorkerListView, TaskListView, PositionListView

urlpatterns = [
    path("", index, name="index"),
    path("task-types", TaskTypeListView.as_view(), name="task-type-list"),
    path("positions", PositionListView.as_view(), name="position-list"),
    path("workers", WorkerListView.as_view(), name="worker-list"),
    path("tasks", TaskListView.as_view(), name="task-list"),
]

app_name = "tasks"
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic

from tasks.models import TaskType, Position, Task, Worker


# @login_required
def index(request):
    """View function for the home page of the site."""

    num_task_types = TaskType.objects.all().count()
    num_positions = Position.objects.all().count()
    num_workers = get_user_model().objects.all().count()
    num_tasks = Task.objects.all().count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_task_types": num_task_types,
        "num_positions": num_positions,
        "num_workers": num_workers,
        "num_tasks": num_tasks,
    }

    return render(
        request,
        "tasks/index.html",
        context=context
    )

class TaskTypeListView(generic.ListView):
    model = TaskType
    template_name = "tasks/task_type_list.html"
    context_object_name = "task_type_list"


class PositionListView(generic.ListView):
    model = Position


class WorkerListView(generic.ListView):
    model = Worker
    paginate_by = 5


class TaskListView(generic.ListView):
    model = Task
    paginate_by = 5
    queryset = Task.objects.all().select_related("task_type")


from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from tasks.forms import WorkerCreationForm, TaskForm, TaskTypeSearchForm, PositionSearchForm, TaskSearchForm, WorkerSearchForm
from tasks.models import TaskType, Position, Task, Worker


@login_required
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

class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "tasks/task_type_list.html"
    context_object_name = "task_type_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = TaskType.objects.all()
        form = TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("tasks:task-type-list")
    template_name = "tasks/task_type_form.html"


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("tasks:task-type-list")
    template_name = "tasks/task_type_form.html"


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("tasks:task-type-list")
    template_name = "tasks/task_type_confirm_delete.html"


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Position.objects.all()
        form = PositionSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("tasks:position-list")

class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("tasks:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("tasks:position-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = WorkerSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["name"])
        return queryset


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm

class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    fields = ("username", "first_name", "last_name", "email", "position",)


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("tasks:worker-list")
class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Task.objects.all().select_related("task_type")
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")

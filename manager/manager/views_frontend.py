

# Create your views here.


from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import AddTaskForm, EditTaskForm, ManagerSettings, SettingsForm
from .models import Gpus, Nodes, Task

# from .forms import TaskForm, NodeForm

class BaseListView(ListView):
    """
    Bazowy widok listy, z którego będą dziedziczyć inne widoki list.
    """
    context_object_name = 'items'
    paginate_by = 10  # Dodaj paginację, jeśli listy będą długie.

class TasksListView(BaseListView):
    model = Task
    template_name = 'manager/task_list.html'

    def get_queryset(self):
        # Możesz dostosować to, aby zwracało queryset w zależności od potrzeb
        return Task.objects.all().order_by('submit_time')

    def get_context_data(self, **kwargs):
        # Pobierz istniejący kontekst z klasy bazowej
        context = super().get_context_data(**kwargs)
        # Dodaj dodatkowe dane do kontekstu
        context['waiting_tasks'] = Task.objects.filter(status='Waiting')
        context['pending_tasks'] = Task.objects.filter(status='Pending')
        context['active_tasks'] = Task.objects.filter(Q(status='Running') | Q(status='Interrupted'))
        context['finished_tasks'] = Task.objects.filter(status='Finished')

        return context

class TasksAddView(CreateView):
    model = Task
    form_class = AddTaskForm  # Użyj swojego formularza TaskForm
    template_name = 'manager/task_form.html'  # Nazwij swój szablon formularza
    success_url = reverse_lazy('task-list')  # Przekieruj po pomyślnym dodaniu zadania

    def form_valid(self, form):
        # Tutaj możesz dodać dodatkową logikę po walidacji formularza
        return super().form_valid(form)

class TaskUpdateView(UpdateView):
    model = Task
    form_class = EditTaskForm
    template_name = 'manager/edit_task.html'  # Nazwa szablonu formularza edycji
    success_url = reverse_lazy('task-list')  # URL przekierowania po pomyślnej edycji

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        # Możesz dodać dodatkową logikę przed zapisem formularza, jeśli jest potrzebna
        return super().form_valid(form)

class NodesListView(BaseListView):
    model = Task
    template_name = 'manager/node_list.html'

    def get_queryset(self):
        # Możesz dostosować to, aby zwracało queryset w zależności od potrzeb
        return Nodes.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        # Pobierz istniejący kontekst z klasy bazowej
        context = super().get_context_data(**kwargs)
        # Dodaj dodatkowe dane do kontekstu
        context['waiting_tasks'] = Nodes.objects.filter(status='Waiting')
        context['pending_tasks'] = Nodes.objects.filter(status='Pending')
        context['active_tasks'] = Nodes.objects.filter(Q(status='Running') | Q(status='Interrupted'))
        context['finished_tasks'] = Nodes.objects.filter(status='Finished')

        return context

class GpusListView(BaseListView):
    model = Task
    template_name = 'manager/gpu_list.html'

    def get_queryset(self):
        # Możesz dostosować to, aby zwracało queryset w zależności od potrzeb
        return Gpus.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        # Pobierz istniejący kontekst z klasy bazowej
        context = super().get_context_data(**kwargs)
        # Dodaj dodatkowe dane do kontekstu
        context['waiting_tasks'] = Gpus.objects.filter(status='Waiting')
        context['pending_tasks'] = Gpus.objects.filter(status='Pending')
        context['active_tasks'] = Gpus.objects.filter(Q(status='Running') | Q(status='Interrupted'))
        context['finished_tasks'] = Gpus.objects.filter(status='Finished')

        return context

class SettingsView(UpdateView):
    model = ManagerSettings
    form_class = SettingsForm
    template_name = 'manager/manager_settings.html'
    success_url = reverse_lazy('managersettings')

    def get_object(self, queryset=None):
        # Pobierz obiekt ManagerSettings lub zwróć 404 jeśli nie istnieje
        return ManagerSettings.objects.first()

    def form_valid(self, form):
        # Logika po pomyślnym zapisaniu formularza
        from manager.components.scheduler import ThreadedScheduler

        from .components.queue import QueueManager
        queue_watchdog_value = form.cleaned_data["queue_watchdog"]
        if queue_watchdog_value is True:
            try:
                scheduler = (
                    ThreadedScheduler.get_instance()
                )  # Pobierz instancję schedulera
                scheduler.every(1).seconds.do(QueueManager().schedule_tasks)
                scheduler.start()  # Uruchom scheduler, jeśli nie jest już uruchomiony
            except Exception as e:
                print(e)
        else:
            try:
                scheduler = (
                    ThreadedScheduler.get_instance()
                )  # Pobierz instancję schedulera
                scheduler.stop()  # Uruchom scheduler, jeśli nie jest już uruchomiony
            except Exception as e:
                print(e)
        return super().form_valid(form)

class ConsoleView(BaseListView):
    model = Task
    template_name = 'manager/console.html'




# Create your views here.


from django.db.models import Q
from django.views.generic import ListView

from .models import Nodes, Task

# from .forms import TaskForm, NodeForm

class BaseListView(ListView):
    """
    Bazowy widok listy, z którego będą dziedziczyć inne widoki list.
    """
    context_object_name = 'items'
    paginate_by = 10  # Dodaj paginację, jeśli listy będą długie.

class TaskListView(BaseListView):
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

class NodeListView(BaseListView):
    model = Nodes
    template_name = 'manager/node_list.html'

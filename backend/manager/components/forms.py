from django import forms
from common_models.models import Task
from django.core.exceptions import ValidationError
import re
from datetime import timedelta
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML
from common_models.models import ManagerSettings

class EditTaskForm(forms.ModelForm):
    pass
    class Meta:
        model = Task
        fields = ['path', 'priority', 'status']
        widgets = {
            'path': forms.TextInput(attrs={'class': 'form-control'}),
            'node_name': forms.TextInput(attrs={'class': 'form-control'}),
            'port': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'error_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(EditTaskForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
        
class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['path', 'priority', 'gpu_partition', 'est']
        widgets = {
            'path': forms.TextInput(attrs={'class': 'form-control'}),  # Upewnij się, że to TextInput
            'priority': forms.Select(choices=[('slow', 'Slow'), ('normal', 'Normal'), ('fast', 'Fast')], attrs={'class': 'form-control'}),
            'gpu_partition': forms.Select(choices=[('normal', 'Normal'), ('high', 'High')], attrs={'class': 'form-control'}),
            'est': forms.TextInput(attrs={'class': 'form-control'}),  # Jeśli est jest czasem, możesz potrzebować specjalnego widgetu
        }
        help_texts = {
            'est': 'Estimated simulation time (in hours)'
        }

    def __init__(self, *args, **kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
            
 
class SettingsForm(forms.ModelForm):
    class Meta:
        model = ManagerSettings
        fields = ["queue_watchdog"]

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('queue_watchdog', wrapper_class='form-check form-switch'),
                    HTML('<label class="form-check-label" for="id_queue_watchdog">Default switch checkbox input</label>'),
                    css_class='form-check form-switch',
                ),
                css_class='row',
            ),
        )
        self.helper.form_method = 'post'

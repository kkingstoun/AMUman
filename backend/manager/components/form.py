from django import forms
from common_models.models import Task
from django.core.exceptions import ValidationError
import re
from datetime import timedelta

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['path', 'node_name', 'port', 'start_time', 'end_time', 'error_time', 'priority', 'status']
        widgets = {
            'path': forms.TextInput(attrs={'class': 'form-control'}),
            'node_name': forms.TextInput(attrs={'class': 'form-control'}),
            'port': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'error_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
        self.fields['status'].disabled = True
        self.fields['end_time'].disabled = True
        self.fields['error_time'].disabled = True
        self.fields['start_time'].disabled = True
        self.fields['node_name'].disabled = True
        self.fields['port'].disabled = True
        
class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['path', 'priority', 'gpu_partition', 'est']
        widgets = {
            'path': forms.TextInput(attrs={'class': 'form-control'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control'}),
            'gpu_partition': forms.Select(choices=[('normal', 'Normal'), ('high', 'High')], attrs={'class': 'form-control'}),
            'est': forms.TextInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'est': 'Estimated simulation time (in hours)'
        }

    def __init__(self, *args, **kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
        # self.fields['end_time'].disabled = True
        # self.fields['error_time'].disabled = True
        # self.fields['start_time'].disabled = True
        # self.fields['node_name'].disabled = True
        # self.fields['port'].disabled = True
        
    def clean_est(self):
            est = self.cleaned_data['est']
            # Sprawdź, czy wartość jest w odpowiednim formacie
            match = re.match(r'^(\d+):(\d{2}):(\d{2})$', str(est))
            if not match:
                raise ValidationError('Invalid time format. Use HH:MM:SS format.')

            hours, minutes, seconds = map(int, match.groups())
            return timedelta(hours=hours, minutes=minutes, seconds=seconds)
 
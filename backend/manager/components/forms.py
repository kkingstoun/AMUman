from django import forms
from common_models.models import Task
from django.core.exceptions import ValidationError
import re
from datetime import timedelta

class EditTaskForm(forms.ModelForm):
    pass
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
        super(EditTaskForm, self).__init__(*args, **kwargs)
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


    # def clean_est(self):
    #     est = self.cleaned_data['est']
    #     # Sprawdź, czy est jest już obiektem timedelta
    #     if isinstance(est, timedelta):
    #         return est
    #     # Jeśli est jest ciągiem znaków, przetwórz go
    #     try:
    #         hours, minutes, seconds = [int(part) for part in est.split(':')]
    #         return timedelta(hours=hours, minutes=minutes, seconds=seconds)
    #     except ValueError:
    #         # Możesz tu dodać jakąś logikę obsługi błędów lub po prostu zwrócić None
    #         return None

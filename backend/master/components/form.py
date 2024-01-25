from django import forms
from common_models.models import Task

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

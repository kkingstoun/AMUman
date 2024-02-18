# from django import forms
# from django.contrib.auth.forms import UserChangeForm
# from django.contrib.auth.models import User
# from .models import Profile

# class CustomUserChangeForm(UserChangeForm):
#   class Meta:
#         model = Profile
#         fields = ['concurrent_jobs']
#         widgets = {
#             'concurrent_jobs': forms.Select(choices=Profile.ConcurrentJobs.choices),
#         }
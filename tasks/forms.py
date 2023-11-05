from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import Task

# User = get_user_model()

# class CustomLoginForm(forms.Form):
#     email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
#     password = forms.CharField(widget=forms.PasswordInput)

#     def clean(self):
#         cleaned_data = super().clean()
#         email = cleaned_data.get('email')
#         password = cleaned_data.get('password')
#         print('email: ', email)
#         print('password: ', password)

#         if email and password:
#             user = authenticate(email=email, password=password)
#             print('user auth forms: ', user)

#             if user is None:
#                 raise forms.ValidationError('Invalid email or password')

#         return cleaned_data

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'due_date', 'priority', 'photos', 'description']


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'photos']
    

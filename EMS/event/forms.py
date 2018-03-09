from django import forms
from django.contrib.auth.models import User

from .models import Event, Profile, Ticket


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'location', 'date', 'time']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
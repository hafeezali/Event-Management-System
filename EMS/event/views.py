from django.shortcuts import render
from .models import Event, Profile, Ticket

def index(request):
    events = Event.objects.all()


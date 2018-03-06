from django.shortcuts import render
from .models import Event, Profile, Ticket
from django.db.models import Q


def home(request):
    events = Event.objects.all()
    query = request.GET.get("query")
    if query:
        events = events.filter(
            Q(name__icontains=query) |
            Q(manager__first_name__icontains=query) |
            Q(manager__last_name__icontains=query)
        ).distinct()
        return render(request, 'event/home.html', {
            'events': events,
        })
    else:
        return render(request, 'event/home.html', {
            'events': events,
        })

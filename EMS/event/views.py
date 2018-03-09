from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .models import Event, Profile, Ticket
from .forms import EventForm, UserForm


def home(request):
    events = Event.objects.all()
    query = request.GET.get("query")
    if query:
        events = events.filter(
            Q(name__icontains=query) |
            Q(manager__first_name__icontains=query) |
            Q(manager__last_name__icontains=query)
        ).distinct()
        return render(request, './event/home.html', {
            'events': events,
            'query': query,
        })
    else:
        return render(request, './event/home.html', {
            'events': events,
            'query': query,
        })


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                events = Event.objects.all()
                return render(request, 'event/home.html', {'events': events})
    context = {
        "form": form,
    }
    return render(request, 'event/register.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                events = Event.objects.all()
                return render(request, 'event/index.html', {'events': events})
            else:
                return render(request, 'event/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'event/login.html', {'error_message': 'Invalid login'})
    return render(request, 'event/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'event/login.html', context)
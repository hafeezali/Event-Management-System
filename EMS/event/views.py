from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User

from .models import Event, Profile, Ticket
from .forms import EventForm, UserForm, ProfileForm

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'event/login.html')
    else:
        events = Event.objects.all()
        query = request.GET.get("query")
        if query:
            events = events.filter(
                Q(name__icontains=query) |
                Q(manager__first_name__icontains=query) |
                Q(manager__last_name__icontains=query)
            ).distinct()
            return render(request, './event/home.html', {
                'user': request.user,
                'events': events,
                'query': query,
            })
        else:
            return render(request, './event/home.html', {
                'user': request.user,
                'events': events,
                'query': query,
            })


def register(request):
    register_form = UserForm(request.POST or None, prefix="register")
    profile_form = ProfileForm(request.POST or None, prefix="profile")
    if register_form.is_valid() and profile_form.is_valid():
        user = register_form.save(commit=False)
        username = register_form.cleaned_data['username']
        password = register_form.cleaned_data['password']
        user.set_password(password)
        user.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.wallet_balance = 0
        profile.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                events = Event.objects.all()
                return render(request, 'event/home.html', {'events': events, 'user': user})
    context = {
        "register_form": register_form,
        "profile_form": profile_form
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
                return render(request, 'event/home.html', {'events': events, 'user': user})
            else:
                return render(request, 'event/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'event/login.html', {'error_message': 'Invalid login'})
    return render(request, 'event/login.html')


def logout_user(request):
    logout(request)
    # form = UserForm(request.POST or None)
    # context = {
    #     "form": form,
    # }
    return render(request, 'event/login.html')


def add_event(request):
    if not request.user.is_authenticated:
        return render(request, 'event/login.html')
    else:
        form = EventForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            event = form.save(commit=False)
            event.manager = request.user
            # Need to add the image part
            # event.image = request.FILES['image']
            # file_type = event.image.url.split('.')[-1]
            # file_type = file_type.lower()
            # if file_type not in IMAGE_FILE_TYPES:
            #     context = {
            #         'event': event,
            #         'form': form,
            #         'error_message': 'Image file must be PNG, JPG, or JPEG',
            #     }
            #     return render(request, 'event/add_event.html', context)
            event.save()
            return render(request, 'event/detail.html', {'event': event})
        context = {
            "form": form,
        }
        return render(request, 'event/add_event.html', context)


def detail(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'event/login.html')
    else:
        user = request.user
        event = get_object_or_404(Event, pk=pk)
        return render(request, 'event/detail.html', {'event': event, 'user': user})


class UpdateEvent(UpdateView):
    model = Event
    fields = ['name', 'location', 'date', 'time']


def get_user_profile(request, pk):
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user_id=pk)
    return render(request, 'event/user_profile.html', {'user': user, 'profile': profile})

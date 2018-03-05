from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Event(models.Model):
    name = models.CharField(max_length=50, null=False)
    image = models.FileField(null=True)
    location = models.TextField(max_length=500, null=False)
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    wallet_pin = models.PositiveIntegerField(null=True)
    wallet_balance = models.PositiveIntegerField(default=0, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Ticket(models.Model):
    attendee = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    fare = models.PositiveIntegerField(null=True)
    flag = models.BooleanField(null=False)

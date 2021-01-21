from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.


class Event(models.Model):
    title       = models.CharField(max_length=150, blank=True, null=True)
    eventdate   = models.DateField()
    description = models.TextField(blank=True, null=True)
    withdraw    = models.BooleanField(default=False)
    user        = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE) # because we are using MODEL_USER_MODEL in settings.py

    def __str__(self):
        return '{} - Event Date : {}'.format(self.title , self.eventdate)
    
    def get_absolute_url(self):
        return reverse("events:edit_event", kwargs={"pk": self.pk})


class Participant(models.Model):
    event = models.ManyToManyField(Event)
    user  = models.ForeignKey('accounts.CustomUser', blank=True, null=True, on_delete=models.CASCADE) 

    def __str__(self):
        return '{}'.format(self.event)
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.db.models import Sum, Max, Count

# Create your models here.
class EventQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_deleted=False)

class EventManager(models.Manager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()


class ParticipantQuerySet(models.query.QuerySet):
    def attended(self):
        return self.filter(attended=True)
    
    def withdraw(self):
        return self.filter(attended=False)
    
    def participants_per_event(self, event):
        count_participant = self.filter(event__id=event, attended=True).aggregate(Count('user')) # to calculate the number of participant of every event
        users_num  = count_participant['user__count']
        # count_participant = self.filter(event__id__in=event).aggregate(Count('user')) # to calculate the number of participant of every event
        return users_num


class ParticipantManager(models.Manager):
    def get_queryset(self):
        return ParticipantQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().attended()


class Event(models.Model):
    title       = models.CharField(max_length=150, blank=True, null=True)
    eventdate   = models.DateField()
    description = models.TextField(blank=True, null=True)
    is_deleted  = models.BooleanField(default=False)
    user        = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE) # because we are using MODEL_USER_MODEL in settings.py
    #participant_count = ParticipantQuerySet.get_count_users #[lambda: Participant.participants_per_event]
    
    objects = EventManager()

    def __str__(self):
        return 'EventID:{} - Title: {} - Date: {} - Owner: {}'.format(
                self.id, self.title , self.eventdate, self.user.username)
    
    def get_absolute_url(self):
        return reverse("events:edit_event", kwargs={'id': self.id})


class Participant(models.Model):
    # event     = models.ManyToManyField(Event, null=True)
    event     = models.ForeignKey(Event, blank=True, null=True, on_delete=models.CASCADE)
    attended  = models.BooleanField(default=False)
    user      = models.ForeignKey('accounts.CustomUser', blank=True, null=True, on_delete=models.CASCADE) 

    objects = ParticipantManager()

    def __str__(self):
        return '{} - {}'.format(self.event, self.user)
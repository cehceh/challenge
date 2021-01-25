from events.models import Event
from django.contrib import admin
from .models import Event, Participant



# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'eventdate', 'description', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('user', 'title', 'eventdate', 'id')


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'attended')
    list_filter = ('attended',)
    search_fields = ('user', 'title', 'event', 'id')



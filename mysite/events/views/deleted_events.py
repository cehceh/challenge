from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
# from django.shortcuts import render, redirect
from django.urls import reverse

from ..models import Event, Participant
# from ..forms import EventForm
from events.tables.tables import EventTable



def delete_event(request, id):
    ''' Delete here means EXCLUDE not completely deletion to enable user to return event again '''
    user_id = request.user.id
    match_attended = Participant.objects.filter(event_id=id).attended().exists()
    if match_attended:
        messages.success(request, 'Someone has attended this event, you can\'t delete it...')
        return redirect(reverse('events:table_event', kwargs={'user': user_id}))
    else:
        Event.objects.filter(id=id).update(is_deleted=True)
    return HttpResponseRedirect(reverse('events:table_event', kwargs={'user': user_id}))

def return_deleted(request, id):
    ''' Return deleted event to enable user to edit this event again '''
    user_id = request.user.id
    Event.objects.filter(id=id).update(is_deleted=False)
    return HttpResponseRedirect(reverse('events:table_event', kwargs={'user': user_id}))


def table_deleted(request, user):
    ''' Table of deleted events to enable users to return deleted events '''
    # user_id = request.user.id
    qs = Event.objects.filter(user=user, is_deleted=True).order_by('-eventdate')
    table = EventTable(qs, exclude='edit, delete')
    table.paginate(page=request.GET.get('page', 1), per_page=10)

    context = {
        'all_deleted_events_table': table,
    }
    return render(request, 'events/tables/all_deleted_events.html', context)


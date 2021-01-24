from django.http.response import HttpResponseRedirect
from django.contrib import messages

from ..models import Event, Participant
from django.shortcuts import render, redirect
# from django.urls import reverse
# from ..forms import ParticipantForm
# from events.tables.tables import ParticipantTable




def join_specific_event(request, event_id, user):
    ''' Handeling Saving an instance of Participant and make join to an event automatically '''
    match_attended = Participant.objects.filter(event_id=event_id, user=user, attended=True).exists()
    match_withdraw = Participant.objects.filter(event_id=event_id, user=user, attended=False).exists()
    if match_attended:
        messages.success(request, "You are already join this event before, choose another event")
        return redirect('/list/all/events')
    elif match_withdraw:
        Participant.objects.filter(event=event_id, user=user).update(attended=True)
    else:
        Participant.objects.create(event_id=event_id, user_id=request.user.id, attended=True)
        # instance = Participant(event_id=event_id, user_id=request.user.id, attended=True)
        # instance.save()

    return HttpResponseRedirect('/list/all/events')#(reverse('events:user_participant_table', kwargs={'user': user}))

def withdraw_specific_event(request, event_id, user):
    ''' Handeling withdrawing automatically '''
    match_withraw = Participant.objects.filter(event=event_id, user=user, attended=False).exists()
    match_attended = Participant.objects.filter(event=event_id, user=user, attended=True).exists()
    if match_withraw:
        messages.success(request, "You are already withdrawed from this event ...")
        return redirect('/list/all/events')
    elif match_attended:
        Participant.objects.filter(event=event_id, user=user).update(attended=False)
    else:
        return redirect('/list/all/events')
        
    return HttpResponseRedirect('/list/all/events')#(reverse('events:user_participant_table', kwargs={'user': user}))

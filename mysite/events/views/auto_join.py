from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from ..models import Event, Participant
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# from ..forms import ParticipantForm
# from events.tables.tables import ParticipantTable



@login_required
def join_specific_event(request, event_id, user):
    ''' Handeling Saving an instance of Participant and make join to an event automatically '''
    # inner = Event.objects.filter(id=event_id, user=user)
    # qs = Participant.objects.filter(event_id=event_id, user=user, attended=True)
    match_attended = Participant.objects.filter(event_id=event_id, user=user, attended=True).exists()
    match_withdraw = Participant.objects.filter(event_id=event_id, user=user, attended=False).exists()
    # if inner not in qs:
    if match_attended:
        messages.success(request, "You are already join event ID (" + str(event_id) + ") before, choose another event")
        return redirect('list_active_events')
    elif match_withdraw:
        Participant.objects.filter(event=event_id, user=user).update(attended=True)
    else:
        Participant.objects.create(event_id=event_id, user_id=request.user.id, attended=True)
        # instance = Participant(event_id=event_id, user_id=request.user.id, attended=True)
        # instance.save()
    # else:
    #     messages.success(request, 'Not Allowed')

    return HttpResponseRedirect(reverse('list_active_events'))#(reverse('events:user_participant_table', kwargs={'user': user}))


@login_required
def withdraw_specific_event(request, event_id, user):
    ''' Handeling withdrawing automatically '''
    # inner = Event.objects.filter(id=event_id, user=user)
    # qs = Participant.objects.filter(event_id=event_id, user=user, attended=False)
    match_withraw = Participant.objects.filter(event=event_id, user=user, attended=False).exists()
    match_attended = Participant.objects.filter(event=event_id, user=user, attended=True).exists()
    # if inner not in qs: 
    if match_withraw:
        messages.success(request, "You are already withdrawed from this event ...")
        return redirect('list_active_events')
    elif match_attended:
        Participant.objects.filter(event=event_id, user=user).update(attended=False)
    else:
        return redirect('list_active_events')
    # else:
    #     messages.success(request, 'Not Allowed')        
    return redirect('list_active_events')#(reverse('events:user_participant_table', kwargs={'user': user}))

from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Sum, Max, Count
from ..models import Event, Participant
from django.shortcuts import render, redirect
from django.urls import reverse
from ..forms import ParticipantForm
from events.tables.tables import ParticipantTable

from datetime import date

from django.contrib.auth import get_user_model
User = get_user_model()


def add_participant(request):
    ''' Handling add participants '''
    user_id = request.user.id
    bound_form = ParticipantForm(data={'user': user_id})
    if request.method == 'POST':
        form = ParticipantForm(request.POST or None)
        # if request.user.id: 
        if form.is_valid():
            event = request.POST.get('event')
            user = request.POST.get('user')
            match_attended = Participant.objects.filter(event_id=event, user=user, attended=True).exists()
            if match_attended:
                messages.success(request, "You are already join this event before, choose another event")
            else:
                form.save()
                return redirect(reverse('events:user_participant_table', kwargs={'user': user_id}))
        # else:
        #     messages.success(request, "You can't add event to another user, choose your user name ")   
        #     return redirect('events:add_participant')
    else:
        form = ParticipantForm

    context = {
        'form': form,
        'boundform': bound_form,
    }
    return render(request, 'events/add_participant.html', context)

def edit_participant(request, id):
    ''' Handling update of Participant '''
    user_id = request.user.id
    match_withraw = Participant.objects.filter(event_id=id, user=user_id, attended=False).exists()
    
    qs = Participant.objects.get(id=id)
    form = ParticipantForm(request.POST or None, instance=qs)
    if form.is_valid():
        if user_id is not None:
            form.save()
            return redirect('events:table_participant')
        else:
            user_id = request.user.id

    context = {
        'form': form,
        'match_withraw': match_withraw,
    }
    return  render(request, 'events/edit_participant.html', context)

def user_participant_table(request, user):
    ''' Handling all participate events for a user '''
    qs = Participant.objects.filter(user=user).attended().order_by('-id')
    table = ParticipantTable(qs)
    table.paginate(page=request.GET.get('page',1), per_page=10)

    context={
        'user_participant_table': table,
    }
    return render(request, 'events/tables/user_participant_table.html', context)


def table_participant(request):
    ''' Handling all attended events for all users '''
    inner = Event.objects.filter(eventdate__lt=date.today())
    qs = Participant.objects.select_related('event').exclude(event_id__in=inner).attended().order_by('-events_event.eventdate')
    # print(qs)
    table = ParticipantTable(qs, exclude='edit, join')
    table.paginate(page=request.GET.get('page',1), per_page=10)
    context={
        'all_participant_table': table,
    }
    return render(request, 'events/tables/all_participant_table.html', context)


def withdraw_table(request, user):
    ''' Method to display all withdraw events of spcefic user '''
    inner = Event.objects.filter(user=user, eventdate__lt=date.today())
    qs = Participant.objects.select_related('event').exclude(event_id__in=inner).filter().withdraw().order_by('-events_event.eventdate')
    
    table = ParticipantTable(qs, exclude='user, withdraw')
    table.paginate(page=request.GET.get('page', 1), per_page=10)
    context = {
        'user_withdraw_table': table,
    }
    return render(request, 'events/tables/withdraw_table.html', context)



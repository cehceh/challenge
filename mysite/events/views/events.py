# from django.core.checks import messages
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

# from django.db.models.aggregates import Count
from django.db.models import Sum, Max, Count

from ..models import Event, Participant
from ..forms import EventForm
from events.tables.tables import EventTable, ParticipantTable

# from django.contrib.auth import get_user_model
# User = get_user_model()

# Create your views here.

def create_event(request):
    ''' Method to handel event creation '''
    # qs = User.objects.values('id').first()
    # name = qs['id']
    # username = request.user.email
    user_id = request.user.id

    bound_form = EventForm(data={'user': user_id}) # to pass a current user to user field in theform
    
    if request.method == 'POST':
        form =  EventForm(request.POST or None)
        if form.is_valid():
            # name = request.POST.get('user')
            # # print(name, user_id, username)
            # if name != request.user.id:
            #     messages.success(request, 'username must be ' + str(username))   
            # else:
            form.save()
            return redirect(reverse('events:table_event', kwargs={'user': user_id}))
    else:
        form = EventForm()

    context = {
        'form': form,
        'boundform': bound_form, 
        }
    return render(request, 'events/create_event.html', context)


def edit_event(request, id):
    ''' Method to handel update to spcefic event '''
    # inner = Event.objects.filter(user=user, is_deleted=False)
    # user = request.user.id
    # event = Event.objects.filter().active()
    # event = Event.objects.get(id=id)
    # event = Event.objects.all()#filter().active()#get(id=id)

    # event = Event.objects.values('id').filter().first()
    # event_id= event['id']
    # # # count_participant = Participant.objects.filter(event__id__in=event).aggregate(Count('user'))
    # count_participant = Participant.objects.values('event').filter(event__id=event_id).aggregate(Count('user')) # this is what we want 
    # part_event = Participant.objects.filter(event__id__in=event, user=user)
    count_users =  Participant.objects.filter().participants_per_event(id)
    # table = ParticipantTable(count_users)
    # table.paginate(page=request.GET.get('page', 1), per_page=5)
    # event = Event.objects.values('id').filter(id=id).first()
    # event_id= event['id']
    # # # count_participant = Participant.objects.filter(event__id__in=event).aggregate(Count('user'))
    # count_participant = Participant.objects.values('event').filter(event__id=event_id).aggregate(Count('user')) # this is what we want 
    # # part_event = Participant.objects.filter(event__id__in=event, user=user)
    # count_user = Participant.objects.filter(user=user).aggregate(Count('user')) # it is not what we want
    # print(count_participant, event, count_user)

    qs = Event.objects.get(id=id)
    event = Event.objects.values('id').filter(id=id).first()
    event_id = event['id']
    form = EventForm(request.POST or None, instance=qs)
    if form.is_valid():
        form.save()
        # return redirect(qs.get_absolute_url())
        return redirect(reverse('events:edit_event', kwargs={'id': event_id}))

    context = {
        'form': form, 
        'count_users': count_users,
        'event': id,    
    }
    return render(request, 'events/edit_event.html', context)


def table_event(request, user):
    ''' Method to display all events of spcefic event '''
    qs = Event.objects.filter(user_id=user, is_deleted=False).order_by('-eventdate')
    table = EventTable(qs, exclude='re_del')
    table.paginate(page=request.GET.get('page', 1), per_page=10)
    context = {
        'user_table': table,
    }
    return render(request, 'events/tables/create_event_table.html', context)    


from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from django.db import transaction, connection
from datetime import date
from ..models import Event, Participant
from ..forms import EventForm
from events.tables.tables import EventTable, ParticipantTable
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import get_user_model
# User = get_user_model()

# Create your views here.

# @login_required
def create_event(request):
    ''' Method to handel event creation '''
    # qs = User.objects.values('id').first()
    # name = qs['id']
    # username = request.user.email
    user_id = request.user.id

    # bound_form = EventForm(data={'user': user_id}) # to pass a current user to user field in theform
    
    if request.method == 'POST':
        form =  EventForm(request.POST or None)
        if form.is_valid():
            saving_form = form.save(commit=False)
            saving_form.user = request.user
            saving_form.title = request.POST.get('title')
            saving_form.eventdate = request.POST.get('eventdate')
            saving_form.description = request.POST.get('description')

            saving_form.save()
            # saving_form.id = request.GET.get('id')
            # Participant.objects.create(event_id=request.GET.get('id'), user_id=user_id, attended=True)
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO events_participant(event_id, attended, user_id)
                            SELECT id, true, user_id 
                            FROM events_event''')
            transaction.commit
            return redirect(reverse('events:table_event', kwargs={'user': user_id}))
    else:
        print('error')
        form = EventForm()

    context = {
        'form': form,
        # 'boundform': bound_form, 
        }
    return render(request, 'events/create_event.html', context)


def edit_event(request, id):
    ''' Method to handel update to spcefic event '''
    user_id = request.user.id
    count_users =  Participant.objects.filter().participants_per_event(id) # Get the amount of participants look at models

    qs = Event.objects.get(id=id)

    form = EventForm(request.POST or None, instance=qs)
    if form.is_valid():
        edit_form = form.save()
        edit_form.user = request.user
        edit_form.save()
        return redirect(reverse('events:table_event', kwargs={'user': user_id}))

    context = {
        'form': form, 
        'count_users': count_users,
        'event': id,    
    }
    return render(request, 'events/edit_event.html', context)


def table_event(request, user):
    ''' Method to display all events of spcefic user '''
    qs = Event.objects.filter(eventdate__gte=date.today(), user_id=user, is_deleted=False).order_by('-eventdate')
    table = EventTable(qs, exclude='re_del, withdraw')
    table.paginate(page=request.GET.get('page', 1), per_page=10)
    context = {
        'user_table': table,
    }
    return render(request, 'events/tables/create_event_table.html', context)    


# from django.contrib import messages
# from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

# from django.db import transaction, connection
from datetime import date
from ..models import Event, Participant
from ..forms import EventForm
from events.tables.tables import EventTable, ParticipantTable
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required   # to force user to be  login and prevent reach to this url without login 
def create_event(request):
    ''' Method to handel event creation '''

    if request.method == 'POST':
        form =  EventForm(request.POST or None)
        if form.is_valid():
            # next lines to save login user automatically with some modification in forms.py  
            saving_form = form.save(commit=False)
            saving_form.user = request.user
            saving_form.title = request.POST.get('title')
            saving_form.eventdate = request.POST.get('eventdate')
            saving_form.description = request.POST.get('description')

            saving_form.save()
            eventid = saving_form.id
            user = saving_form.user.id
            Participant.objects.create(event_id=eventid, user_id=user, attended=True) # to make join to event automatically
            # print(eventid)
            
            # SQL raw is a good stuff if we use 'where' statment but django ORM win
            # cursor = connection.cursor()
            # cursor.execute('''INSERT INTO events_participant(event_id, attended, user_id)
            #                 SELECT id, true, user_id 
            #                 FROM events_event''')
            # transaction.commit
            return redirect(reverse('events:table_event', kwargs={'user': user}))
    else:
        form = EventForm()

    context = {
        'form': form, 
        }
    return render(request, 'events/create_event.html', context)


@login_required
def edit_event(request, id):
    ''' Method to handel update to spcefic event '''

    user_id = request.user.id
    count_users =  Participant.objects.filter().participants_per_event(id) # Get the amount of participants look at models

    qs = Event.objects.get(id=id)

    form = EventForm(request.POST or None, instance=qs)
    if form.is_valid():
        # handeling update login user automatically
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


@login_required
def table_event(request, user):
    ''' Method to display all events of spcefic user '''

    # get all events that is not expire , not deleted for specific user
    qs = Event.objects.filter(eventdate__gte=date.today(), user_id=user, is_deleted=False).order_by('-eventdate')
    
    # control the pagination number  
    page_no = request.GET.get('pageno')
    if page_no == None or page_no == '' or int(page_no) == 0:
        table = EventTable(qs, exclude='re_del')
        table.paginate(page=request.GET.get('page', 1), per_page=10)
    else:
        table = EventTable(qs, exclude='re_del')
        table.paginate(page=request.GET.get('page', 1), per_page=page_no)
    context = {
        'user_table': table,
    }
    return render(request, 'events/tables/create_event_table.html', context)    


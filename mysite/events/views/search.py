from events.tables.tables import EventTable, ParticipantTable
# from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404
from ..models import Event, Participant
from django.db.models import Q

from datetime import datetime, date


@login_required
def search_event_date(request):
    ''' andeling shearch events by date range between two dates '''
    search_from= request.GET.get('from')
    search_to = request.GET.get('to')

    try: # here we catch unformated date 
        if search_from != datetime.strptime(search_from, "%Y-%m-%d").strftime('%Y-%m-%d') or search_from is None:
            raise ValueError
        elif search_to != datetime.strptime(search_to, "%Y-%m-%d").strftime('%Y-%m-%d') or search_to is None:
            raise ValueError
        elif search_from is None or search_to is None:
            return redirect('list_active_events')
        else:
            if search_from != '' and search_to != '':
                search_result = Participant.objects.select_related('event') \
                                            .filter(Q(event__eventdate__range=[search_from, search_to], event__is_deleted=False)) \
                                            .order_by('-events_event.eventdate')
                table = ParticipantTable(search_result, exclude='edit, withdraw')
                table.paginate(page=request.GET.get('page', 1), per_page=10)
            else:
                search_result = Event.objects.filter().active().order_by('-eventdate')
                table = EventTable(search_result, exclude='edit, withdraw, delete,re_del')
                table.paginate(page=request.GET.get('page', 1), per_page=10)

    except ValueError:
        raise Http404("Date format not allowed, try this format '2021-09-30' ")

    context = {
        'search_table': table,        
    }
    return render(request, 'events/tables/search_table.html', context)


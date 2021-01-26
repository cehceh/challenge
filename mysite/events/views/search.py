from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ..models import Event, Participant
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import date


@login_required
def search_event_date(request):
    '''  '''
    today = date.today()
    search_from = request.GET.get('from')
    search_to = request.GET.get('to')
    # search_date = request.GET.get('dt')
    event = Event.objects.filter(eventdate__gte=today).active().order_by('-eventdate') 

    count = Participant.objects.values('event') \
                                .annotate(ncount=Count('user'))\
                                .filter(attended=True)  # to get participants count 
    
    if search_from == '' or search_from is None:
        return redirect('list_active_events')
    elif search_to == '' or search_to is None:
        return redirect('list_active_events')
    elif search_from != '' and search_to != '':
        search_result = Event.objects.filter(Q(eventdate__range=[search_from, search_to])).active().order_by('-eventdate')
        # return redirect('events:search_event')
    else:
        search_result = Event.objects.all().order_by('-eventdate')
    
    ## for give a hint to user if he attended the event or not 
    user_attend = Participant.objects.values('event', 'attended').filter(user=request.user.id)

    ## next lines for paginate all active events
    paginator = Paginator(search_result, 4) 
    page = request.GET.get('page')
    try:
        event_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        event_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        event_page = paginator.page(paginator.num_pages)

    context = {
        'search_result':search_result,
        'event_page': event_page,
        'user_attend': user_attend,
        'page': page,
        'count': count,
        'event': event,
    }
    return render(request, 'events/search/search.html', context)


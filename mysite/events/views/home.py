from events.tables.tables import ParticipantTable
from django.shortcuts import render, redirect
from ..models import Event, Participant
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

def frontpage(request):
    ''' This method to handel frontpage '''
    return render(request, 'frontpage.html', {})

def dashboard(request): 
    ''' Handling dashboard page '''
    return render(request, 'dashboard.html', {})

def list_all_events(request):
    '''  '''
    event = Event.objects.filter().active().order_by('-eventdate')

    count = Participant.objects.values('event') \
                                .annotate(ncount=Count('user'))\
                                .filter(attended=True) 
    paginator = Paginator(event, 3) # 3 events in each page
    page = request.GET.get('page')
    try:
        event_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        event_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        event_page = paginator.page(paginator.num_pages)
    
    # for item in count:
    #     event_id = item['event']
    #     match_withraw = Participant.objects.filter(event_id=event_id, user=user_id, attended=False).exists()
    # print(count, event_id)
    context = {
        'event_page': event_page,
        'page': page,
        'event': event,
        'count': count,
    }
    return render(request, 'home/list_all_events.html', context)
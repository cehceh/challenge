from django.shortcuts import render
from ..models import Event, Participant
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import datetime, date
# from time import timezone
from django.contrib.auth.decorators import login_required


def frontpage(request):
    ''' This method to handel frontpage '''
    return render(request, 'frontpage.html', {})


@login_required
def dashboard(request): 
    ''' Handling dashboard page '''
    return render(request, 'dashboard.html', {})

@login_required
def list_active_events(request):
    ''' Handling display of all events of any user that have created '''
    ################################################  Important Hint   #############################################################################
    ## in templates we have made 'for' statement to loop all event_id to get all attended events in order to show withdraw button in active events page ##
    ## in templates we have made for statement to loop all event_id to get all withdraw events in order to show join button  in active events page      ##
    ## but i think the right way is displaying a message to the user tell him that is already join the event or not                                     ##
    ##                                                                                                                                                  ##
    ## I already do that in auto_join.py to display a message tell the user if he joined the event or not                                                ##
    ################################################################################################################################################
    user_id = request.user.id
    event_time = date.today()#datetime.now()  # or you can use ==>>  date.today()
    # .active() means not deleted take a look at models.py
    event = Event.objects.filter(eventdate__gte=event_time).active().order_by('-eventdate') 

    count = Participant.objects.values('event') \
                                .annotate(ncount=Count('user'))\
                                .filter(attended=True)  # to get participants count 
    print(event)
    paginator = Paginator(event, 4) 
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
        # 'get_withdraw': get_withdraw,
        # 'get_attended': get_attended,
        'event_page': event_page,
        'page': page,
        'count': count,
    }
    return render(request, 'home/list_active_events.html', context)

@login_required
def list_expire_events(request):
    '''  '''
    today = date.today()
    # event_time = timezone.now().date()
    expire_events = Event.objects.filter(eventdate__lt=today).order_by('-eventdate')
    
    paginator = Paginator(expire_events, 4) 
    page = request.GET.get('page')

    try:
        event_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        event_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        event_page = paginator.page(paginator.num_pages)

    count = Participant.objects.values('event') \
                                .annotate(ncount=Count('user'))\
                                .filter(attended=True)  # to get participants count 
    # print(expire_events)
    context= {
        'event_page': event_page,
        'page': page,
        'count': count,
    }
    return render(request, 'home/list_expire_events.html', context)
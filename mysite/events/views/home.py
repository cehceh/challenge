from events.tables.tables import ParticipantTable
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
    
    ################################################################################################################################################
    user_id = request.user.id
    event_time = date.today()#datetime.now()  # or you can use ==>>  date.today()

    ## .active() means not deleted take a look at models.py
    event = Event.objects.filter(eventdate__gte=event_time).active().order_by('-eventdate') 

    count = Participant.objects.values('event') \
                                .annotate(ncount=Count('user'))\
                                .filter(attended=True)  # to get participants count 

    ## for give a hint to user if he attended the event or not 
    user_attend = Participant.objects.values('event', 'attended').filter(user=user_id)  
    # print()

    ## next lines for paginate all active events
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
        'user_attend': user_attend,
        'event_page': event_page,
        'page': page,
        'count': count,
    }
    return render(request, 'home/list_active_events.html', context)


@login_required
def list_expire_events(request):
    ''' Handeling expire events for all users '''
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


# @login_required
# def user_active_events(request, user): # 
#     ''' Handleing all active(not expire) events and attended for a specific user '''
#     inner = Event.objects.filter(user=user, eventdate__lt=date.today())
#     qs = Participant.objects.select_related('event').exclude(event_id__in=inner).filter(user=user).attended().order_by('-events_event.eventdate')
    
#     table = ParticipantTable(qs, exculde='edite')
#     table.paginate(page=request.GET.get('page', 1), per_page=10)
#     context = {
#         'user_active_events_table': table,
#     }
#     return render(request, 'home/tables/user_active_events.html', context)


@login_required
def user_expire_events(request, user):
    ''''''
    inner = Event.objects.filter(user=user, eventdate__gte=date.today())
    qs = Participant.objects.select_related('event').exclude(event_id__in=inner).filter(user=user).order_by('-events_event.eventdate')
    
    table = ParticipantTable(qs, exculde='edite')
    table.paginate(page=request.GET.get('page', 1), per_page=10)
    context = {
        'user_expire_events_table': table,
    }
    return render(request, 'events/tables/user_expire_events.html', context)

# from django.core.checks import messages
from django.contrib import messages
from django.http.response import HttpResponseRedirect

from events.tables import tables
from ..models import Event
from django.shortcuts import render, redirect
from django.urls import reverse
from ..forms import EventForm
from events.tables.tables import EventTable

# from django.contrib.auth import get_user_model
# User = get_user_model()

# Create your views here.
def frontpage(request):
    ''' This method to handel frontpage '''
    return render(request, 'frontpage.html', {})


def create_event(request):
    ''' Method to handel event creation '''
    # qs = User.objects.values('id').first()
    # name = qs['id']
    username = request.user.email
    user_id = request.user.id

    bound_form = EventForm(data={'user': user_id})
    
    if request.method == 'POST':
        form =  EventForm(request.POST or None)
        # name = request.POST.get('user')
        # print(name, user_id, username)
        # if name != request.user.id:
        #     messages.success(request, 'usrname must be ' + str(username))   
        # else:
        if form.is_valid():
            form.save()
            # return redirect('/events/table/event/user/' + str(user_id) + '/')
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
    qs = Event.objects.get(id=id)
    form = EventForm(request.POST or None, instance=qs)
    if form.is_valid():
        form.save()
        return redirect(qs.get_absolute_url)
        # return redirect(reverse('events:edit_event', kwargs={'id': qs}))

    context = {'form': form,}
    return render(request, 'events/edit_event.html', context)


def table_event(request, user):
    ''' Method to display all events of spcefic event '''
    qs = Event.objects.filter(user_id=user).order_by('-eventdate')
    table = EventTable(qs)
    table.paginate(page=request.GET.get('page', 1), per_page=10)
    context = {
        'user_table': table,
    }
    return render(request, 'events/tables.html', context)    


def delete_event(request, id):
    qs = Event.objects.get(id=id)
    user_id = request.user.id
    qs.delete()
    return HttpResponseRedirect(reverse('events:table_event', kwargs={'user': user_id}))

from django.http.response import HttpResponseRedirect
from events.models import Event
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import EventForm

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def frontpage(request):
    ''' This method to handel frontpage '''
    return render(request, 'frontpage.html', {})


def create_event(request):
    ''' Method to handel event creation '''
    qs = User.objects.values('id').first()
    name = qs['id']
    username = request.user.id
    # if request.user.is_authenticated():
    #     username = request.user.username
    
    bound_form = EventForm(data={'user': username})
    print(name, username)
    if request.method == 'POST':
        form =  EventForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('frontpage')
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
    context = {}
    return render(request, 'events/edit_events.html', context)    


def delete_event(request, id):
    qs = Event.objects.get(id=id)

    qs.delete()
    return HttpResponseRedirect(reverse(''))

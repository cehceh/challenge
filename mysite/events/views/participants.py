from django.forms import boundfield
from django.http.response import HttpResponseRedirect
from ..models import Event, Participant
from django.shortcuts import render, redirect
from django.urls import reverse
from ..forms import ParticipantForm

from django.contrib.auth import get_user_model
User = get_user_model()


def add_participant(request):
    ''' Handling add participants '''
    user_id = request.user.id
    bound_form = ParticipantForm(data={'user': user_id})
    if request.method == 'POST':
        form = ParticipantForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ParticipantForm

    context = {
        'form': form,
        'boundform': bound_form,
    }
    return render(request, 'events/participants.html', context)


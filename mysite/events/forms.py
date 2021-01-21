from datetime import datetime

from django.forms.widgets import Select
from mysite.settings import AUTH_USER_MODEL
from django import forms
from django.forms import fields
from .models import Event, Participant
from datetime import date 

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class EventForm(forms.ModelForm):
    CHOICE_WITHDRAW = (
        (True, 'Continue'),
        (False, 'Withdraw'),
    )
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True, label='User Name',
                            widget=forms.Select(
                                attrs={
                                    'class': 'form-control',
                                })
    )

    title = forms.CharField(required=True, label='Event Title',
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'type': 'text',
                                    'placeholder': 'Write a suitable Title for your event .... ',
                                })
    )

    eventdate = forms.DateField(required=True, label='Event Date',
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'type': 'text',
                                    'value': date.today(),
                                })
    )

    description = forms.CharField(required=False, label='Description',
                            widget=forms.Textarea(
                                attrs={
                                    'class': 'form-control',
                                    'type': 'text',
                                    'placeholder': 'Write a detailed description for your event ....',
                                })
    )

    withdraw = forms.ChoiceField(required=True, label='Withdraw',choices=CHOICE_WITHDRAW,
                                widget=forms.Select(
                                    attrs={
                                        'class': 'form-control',
                                    }))
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     title = cleaned_data.get('title')
    #     eventdate = cleaned_data.get('eventdate')
    #     description = cleaned_data.get('description')

    #     return cleaned_data

    class Meta:
        model = Event
        fields = ('__all__') #('title', 'eventdate', 'description', 'withdraw')


class ParticipantForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True, label='User Name',
                                widget=forms.Select(
                                    attrs={
                                        'class': 'form-control'
                                })
    )
    event = forms.ModelMultipleChoiceField(queryset=Event.objects.all().order_by('-eventdate'), required=True, label='Choose one or more Events', 
                                widget=forms.SelectMultiple(
                                    attrs={
                                        'class': 'form-control'
                                })
    )
    class Meta:
        model = Participant
        fields = ('__all__')
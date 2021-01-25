from mysite.settings import AUTH_USER_MODEL
from django import forms
from .models import Event, Participant
from datetime import date 
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
User = get_user_model()



class EventForm(forms.ModelForm):
   
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
    

    class Meta:
        model = Event
        fields =  ('user', 'title', 'eventdate', 'description',) 

    def __init__(self, *args, **kwargs):
        # self.user = user
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['class'] = 'form-control'
        self.fields['user'].queryset = User.objects.all()


class ParticipantForm(forms.ModelForm):
    CHOICE_WITHDRAW = (
        (True, 'Attend'),
        (False, 'Withdraw'),
    )

    attended = forms.ChoiceField(required=True, label='Attend',choices=CHOICE_WITHDRAW,
                                widget=forms.Select(
                                    attrs={
                                        'class': 'form-control',
                                    }))

    class Meta:
        model = Participant
        # exclude = ["user",]
        fields = ('event', 'attended')
        

    def __init__(self, *args, **kwargs):
        super(ParticipantForm, self).__init__(*args, **kwargs)
        self.fields['event'].widget.attrs['class'] = 'form-control'
        self.fields["event"].queryset = Event.objects.filter(is_deleted=False)
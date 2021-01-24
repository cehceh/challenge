from mysite.settings import AUTH_USER_MODEL
from django import forms
from .models import Event, Participant
from datetime import date 
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
User = get_user_model()



class EventForm(forms.ModelForm):
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
    CHOICE_WITHDRAW = (
        (True, 'Attend'),
        (False, 'Withdraw'),
    )

    attended = forms.ChoiceField(required=True, label='Attend',choices=CHOICE_WITHDRAW,
                                widget=forms.Select(
                                    attrs={
                                        'class': 'form-control',
                                    }))

    # def clean(self):
    #     self.cleaned_data = super().clean()
    #     self.event = self.cleaned_data.get('event_id')
    #     # user = self.cleaned_data.get('user')
    #     # attended = cleaned_data.get('attended')
    #     # inner = Event.objects.values('id').filter(id=event).first()
    #     # inner = Event.objects.all()[0]#filter(id=self.event)
    #     # match_user = Participant.objects.filter(user_id=user).exists()
        
    #     # if user == auth_user:
    #     #     self.add_error('user', 'Not allowed')
    #     #     raise ValidationError('This is not you, choose your user name')
    #     # else:
    #     #     print(auth_user, user)

    #     return self.cleaned_data

    class Meta:
        model = Participant
        # exclude = ["user",]
        fields = ('event', 'attended')
        

    def __init__(self, *args, **kwargs):
        super(ParticipantForm, self).__init__(*args, **kwargs)
        self.fields['event'].widget.attrs['class'] = 'form-control'
        self.fields["event"].queryset = Event.objects.filter(is_deleted=False)
from django.urls import path
from events.views.events import create_event, edit_event, delete_event, table_event
from events.views.participants import add_participant

app_name = 'events'
urlpatterns = [
    path('create/event/', create_event, name='create_event'),
    path('edit/event/<int:id>/', edit_event, name='edit_event'),
    
    path('table/event/user/<int:user>/', table_event, name='table_event'),
    
    path('delete/event/<int:id>/', delete_event, name='delete_event'),

    # for participants
    path('add/participant/', add_participant, name='add_participant'),

]

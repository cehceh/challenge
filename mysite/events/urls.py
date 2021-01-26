from django.urls import path
from events.views.events import create_event, edit_event, table_event
from events.views.participants import (add_participant, edit_participant, table_participant,
                                        user_participant_table, withdraw_table)
from events.views.deleted_events import delete_event, return_deleted, table_deleted 
from events.views.auto_join import join_specific_event, withdraw_specific_event

app_name = 'events'
urlpatterns = [
    # for event add, edit 
    path('create/event/', create_event, name='create_event'),
    path('edit/event/<int:id>/', edit_event, name='edit_event'),

    # deleted and return deleted
    path('delete/event/<int:id>/', delete_event, name='delete_event'),
    path('return/deleted/event/<int:id>/', return_deleted, name='return_deleted'),
    path('all/deleted/event/for/user/<int:user>/', table_deleted, name='table_deleted'),

    # table event and withdraw 
    path('all/events/for/user/<int:user>/', table_event, name='table_event'),
    

    # for participants add, edit
    path('add/participant/', add_participant, name='add_participant'),
    path('edit/participant/<int:id>/', edit_participant, name='edit_participant'),
    
    # table participants  
    path('all/attended/events/for/all/users/', table_participant, name='table_participant'),
    path('all/attended/events/for/user/<int:user>/', user_participant_table, name="user_participant_table"),
    path('all/withdraw/events/for/user/<int:user>/', withdraw_table, name='withdraw_table'),

    # join.py
    path('join/specific/event/<int:event_id>/<int:user>/', join_specific_event, name='join_specific_event'),
    path('withdraw/specific/event/<int:event_id>/<int:user>/', withdraw_specific_event, name='withdraw_specific_event'),


]

import django_tables2 as tables
from django.utils.html import format_html
from events.models import Event, Participant
from django.db.models import Count

def countrow(table):
    return len(table.rows)


class EventTable(tables.Table):
    user = tables.TemplateColumn('{{ record.user }}',
        verbose_name=u'User Name',visible=False)

    title = tables.TemplateColumn( '{{record.title}}',
        verbose_name=u'Event Title')

    eventdate = tables.TemplateColumn( '{{record.eventdate}}',
        verbose_name=u'Event Date', footer="Amount of events",)

    description = tables.TemplateColumn('{{record.discription}}',
        verbose_name=u'Discription', visible=False)

    join = tables.TemplateColumn(
        '<a class="btn btn-outline-success" href="{% url \'events:join_specific_event\' record.id record.user_id %}">Join</a>',
        verbose_name=u'Join Event',)
    
    edit = tables.TemplateColumn(
        '<a class="btn btn-outline-primary" href="{% url \'events:edit_event\' record.id %}">Edit Event</a>',
        verbose_name=u'Edit Event',)
    
    withdraw = tables.TemplateColumn(
        '<a class="btn btn-outline-danger" href="{% url \'events:withdraw_specific_event\' record.id record.user_id %}">Withdraw</a>',
        verbose_name=u'Withdraw',)

    delete = tables.TemplateColumn(
        '<a class="btn btn-outline-danger" href="{% url \'events:delete_event\' record.id %}" '
        'onclick="return confirm(\'Are you sure you want to delete this Event ?\')">Delete</a>',
        verbose_name='Delete Event', footer=countrow)

    re_del = tables.TemplateColumn(
        '<a class="btn btn-outline-primary" href="{% url \'events:return_deleted\' record.id %}">Return Delete</a>',
        verbose_name='Return Delete Event', footer=countrow)

    class Meta:
        model = Event
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('user', 'title', 'eventdate', 'description', 'join', 'edit', 'delete', 're_del')

class ParticipantTable(tables.Table):
    def render_participants(self, value):
        # count_participant = Participant.objects.values('event').filter(event__id=event_id).aggregate(Count('user')) # this is what we want 
        count = Participant.objects.values('event') \
                                    .annotate(ncount=Count('user'))\
                                    .filter(attended=True)
        value = (c.ncount for c in count)
        return ("<b>{}</b>", value)


    user = tables.TemplateColumn('{{record.user.username}}', 
        verbose_name=u'Joined User Name',)

    join = tables.TemplateColumn(
        '<a class="btn btn-outline-success" href="{% url \'events:join_specific_event\' record.event_id record.user_id %}">Join</a>',
        verbose_name=u'Join Event',)

    withdraw = tables.TemplateColumn(
        '<a class="btn btn-outline-danger" href="{% url \'events:withdraw_specific_event\' record.event_id record.user_id %}">Withdraw</a>',
        verbose_name=u'Withdraw',)

    edit = tables.TemplateColumn(
        '<a class="btn btn-outline-success" href="{% url \'events:edit_participant\' record.id %}">Edit Participant</a>',
        verbose_name=u'Edit Participant',)
    
    # def __init__(self, *args, **kawargs):
    #     super(EventTable, self).__init__(*args, **kawargs)
        


    class Meta:
        model = Participant
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('user', 'event', 'attended', 'join', 'edit')
        
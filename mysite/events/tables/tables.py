import django_tables2 as tables
from events.models import Event



def countrow(table):
    return len(table.rows)


class EventTable(tables.Table):
    user = tables.TemplateColumn('{{ record.user }}',
        verbose_name=u'User Name',visible=False)

    title = tables.TemplateColumn( '{{record.title}}',
        verbose_name=u'Event Title')

    eventdate = tables.TemplateColumn( '{{record.eventdate}}',
        verbose_name=u'Event Date')

    description = tables.TemplateColumn('{{record.discription}}',
        verbose_name=u'Discription', visible=False)

    edit = tables.TemplateColumn(
        '<a class="btn btn-outline-success" href="{% url \'events:edit_event\' record.id %}">Edit Event</a>',
        verbose_name=u'Edit Event')
    delete = tables.TemplateColumn(
        '<a class="btn btn-outline-danger" href="{% url \'events:delete_event\' record.id %}" '
        'onclick="return confirm(\'Are you sure you want to delete this Event ?\')">Delete</a>',
        verbose_name='Delete Event',
    )

    # def countrow(self, table):
    #     return len(table.rows)

    class Meta:
        model = Event
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('user', 'title', 'eventdate', 'description', 'edit', 'delete')

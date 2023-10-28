from django import template

from MeetingSystem_CRUD.models import Event

register = template.Library()


@register.inclusion_tag(filename="MeetingSystem_CRUD/inclusion_tags/EventSubscriptionsCount.html")
def getEventSubscriptionsCount(event_pk):
    return {
        "EventSubscriptionsCount": Event.objects.filter(pk=event_pk)[0].profile_set.all().count(),
            }


@register.inclusion_tag(filename="MeetingSystem_CRUD/inclusion_tags/EventDescriptionPopover.html")
def getEventDescriptionPopover(event_title, event_description):
    return {
        "EventTitle": event_title,
        "EventDescription": event_description,
            }


@register.simple_tag(name="get-string-time")
def ConvertDjangoTime(django_time):

    return str(django_time)




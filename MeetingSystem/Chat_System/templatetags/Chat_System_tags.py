from django import template

from Chat_System.models import ChatRoom, ChatMessage

from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.simple_tag(name="getlast_message")
def getlast_message(current_chat_room, currently_logged_user_pk):

    try:
        last_message = current_chat_room.chatmessage_set.all().latest("id")

        if last_message.message_sender == currently_logged_user_pk:

            last_message.message_text = "Вы: " + last_message.message_text

        return {"message": last_message.message_text, "datetime": last_message.creation_time, "datetime_empty": False}

    except ObjectDoesNotExist:

        return {"message": "Отправьте первое сообщение!", "datetime": "Нет данных", "datetime_empty": True}


@register.simple_tag(name="get_participant_name")
def get_chat_participant_name(current_chat_room, logged_user_pk):

    if current_chat_room.is_two_user_chat:
        return current_chat_room.participants.exclude(id=logged_user_pk)[0].username


@register.simple_tag(name="get_participant_user_instance")
def get_chat_participant_instance(current_chat_room, logged_user_pk):

    if current_chat_room.is_two_user_chat:
        return current_chat_room.participants.exclude(id=logged_user_pk)[0]

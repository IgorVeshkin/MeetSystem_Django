from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.core.exceptions import ObjectDoesNotExist

from .models import ChatRoom, ChatMessage, CurrentlyDeletedMessages, CurrentlyEditedMessages

from Registration_Login_App.models import User

from django.core.paginator import Paginator

from MeetingSystem_CRUD.views import logged_user_required, admin_required

# Create your views here.


# @login_required


@logged_user_required
def chats_main(request):

    # print("Hello World")

    # user_chats = ChatRoom.objects.all()

    # user_chats = ChatRoom.objects.filter(participants=request.user)

    pagination = Paginator(ChatRoom.objects.filter(participants=request.user), 10)

    pagonation_link = "current_page"

    current_page = request.GET.get(pagonation_link)

    user_chats = pagination.get_page(current_page)

    # ChatRoom.objects.filter(participants__id__in=[request.user.id])

    context = {
        "user_chats": user_chats,
        "pagonation_link": pagonation_link,
    }

    return render(request, "Chat_System/Chats_main_page.html", context=context)


def create_chat(request, user_pk):
    # print('Hello World 2')

    participants = User.objects.filter(id__in=[request.user.id, user_pk])

    print(participants)

    chat_room = ChatRoom.objects.filter(participants=participants[0]).filter(participants=participants[1])

    if ChatRoom.objects.filter(participants=participants[0]).filter(participants=participants[1]).exists():
        print("Works", ChatRoom.objects.filter(participants=participants[0]).filter(participants=participants[1]))

        return redirect('show-chat', chat_pk=chat_room[0].pk)

    # print("Does ChatRooms exist", ChatRoom.objests.filter(participants__in=participants).exists())

    new_chat = ChatRoom(room_title="")

    new_chat.save()

    new_chat.participants.set(participants)

    new_chat.save()

    # print(new_chat.id)

    # return render(request, "Chat_System/Chats_main_page.html", context={})

    return redirect('show-chat', chat_pk=new_chat.pk)


def show_chat(request, chat_pk):

    deleted_messages = CurrentlyDeletedMessages.objects.filter(chatroom__id=chat_pk).exclude(
        message_sender=request.user)

    deleted_messages.delete()

    edited_messages = CurrentlyEditedMessages.objects.filter(chatroom__id=chat_pk).exclude(
        message_editor=request.user)

    edited_messages.delete()

    try:
        current_chatroom = ChatRoom.objects.get(id=chat_pk)
        current_chatroom_messages = current_chatroom.chatmessage_set.all().order_by('id')

    except ObjectDoesNotExist:
        current_chatroom = {}

    context = {

        "current_chatroom": current_chatroom,

        "chatroom_messages": current_chatroom_messages,

        "chatroom_messages_count": current_chatroom_messages.count(),

    }

    return render(request, "Chat_System/ChatRoom_page.html", context=context)


def send_message(request):
    current_chat = request.GET.get("current_chat")
    message_text = request.GET.get("message_text")
    message_sender = request.GET.get("message_sender")

    new_message = ChatMessage.objects.create(chatroom=ChatRoom.objects.get(id=int(current_chat)),
                                             message_text=message_text,
                                             message_sender=User.objects.get(id=message_sender),)

    response = {
        "message_id": new_message.id,
        "message_text": new_message.message_text,
        "message_sender": new_message.message_sender.username,
        "creation_time": new_message.creation_time

    }

    return JsonResponse(response, safe=False)


def delete_message(request):

    try:

        deleted_message_id = int(request.GET.get("message_id"))

        deleted_message = ChatMessage.objects.get(id=deleted_message_id)

        CurrentlyDeletedMessages.objects.create(deleted_message_id=deleted_message_id,
                                                chatroom=ChatRoom.objects.get(id=int(request.GET.get("chatroom_id"))),
                                                message_sender=User.objects.get(id=int(request.GET.get("message_sender_id")))
                                                )

        deleted_message.delete()

    except:
        pass

    response = {

        "response_text": "Message has been successfully deleted!",

    }

    return JsonResponse(response, safe=False)


def edit_message(request):

    edited_message_id = int(request.GET.get("message_id"))

    edited_message = ChatMessage.objects.get(id=edited_message_id)

    edited_message.message_text = request.GET.get("message_edited_text")
    edited_message.is_message_edited = True

    # edited_message.is_message_edited = True

    edited_message.save()

    current_chatroom = ChatRoom.objects.get(id=int(request.GET.get("current_chatroom_id")))

    CurrentlyEditedMessages.objects.create(edited_message_id=edited_message_id,
                                           edited_message_text=edited_message.message_text,
                                           chatroom=current_chatroom,
                                           message_editor=request.user,)

    print("We are in edit section!")

    response = {

        "response_text": "Message has been successfully edited!",
        "message_edited_text": edited_message.message_text,

    }

    return JsonResponse(response, safe=False)


def check_for_new_messages(request):

    messages_count_on_page = int(request.GET.get("messages_count_on_page"))

    current_chatroom = ChatRoom.objects.get(id=int(request.GET.get("current_chat")))

    messages_on_database = current_chatroom.chatmessage_set.all()

    messages_count_on_database = messages_on_database.count()

    if messages_count_on_page == messages_count_on_database:

        # print('Hello World!')

        edited_messages = CurrentlyEditedMessages.objects.filter(chatroom=current_chatroom).\
            exclude(message_editor=request.user)

        if edited_messages.exists():
            response = {

                "response_text": "No new messages!",
                "new_messages_to_display": [],
                "deleted_messages_id": [],
                "edited_messages": list(edited_messages.values("edited_message_id", "edited_message_text")),
                "deleting": False,
                "editing": True,


            }

            return JsonResponse(response, safe=False)

        response = {

            "response_text": "No new messages!",
            "new_messages_to_display": [],
            "deleted_messages_id": [],
            "edited_messages_id": [],
            "deleting": False,
            "editing": False,

        }

        return JsonResponse(response, safe=False)

    elif messages_count_on_page < messages_count_on_database:

        # print('Hello World 2!')

        response = {

            "response_text": "New messages have been spotted!",
            "new_messages_to_display":  list(messages_on_database[messages_count_on_page:messages_count_on_database].values()),
            "deleted_messages_id": [],
            "edited_messages_id": [],
            "deleting": False,
            "editing": False,
            # list(messages_on_database[messages_count_on_page:messages_count_on_database].values())

        }

        print(list(messages_on_database[messages_count_on_page:messages_count_on_database].values()))

        return JsonResponse(response, safe=False)

    else:

        deleted_messages = CurrentlyDeletedMessages.objects.filter(chatroom=current_chatroom).exclude(message_sender=request.user).all()

        print('deleted_messages =', deleted_messages)

        response = {

            "response_text": "Deleted messages have been sent to javascript!",
            "new_messages_to_display": [],
            "deleted_messages_id": list(deleted_messages.values("deleted_message_id")),
            "edited_messages_id": [],
            "deleting": True,
            "editing": False,
            # list(messages_on_database[messages_count_on_page:messages_count_on_database].values())

        }

        return JsonResponse(response, safe=False)


def empty_deleted_messages_table(request):

    # try:

    deleted_message_id = int(request.GET.get("deleted_message_id"))

    CurrentlyDeletedMessages.objects.filter(deleted_message_id=deleted_message_id).delete()

    # except:
        # pass

    response = {

        "response_text": "Deleted Messages Table has been Emptied!"

    }

    return JsonResponse(response, safe=False)


def empty_edited_messages_table(request):

    edited_message_id = int(request.GET.get("edited_message_id"))

    CurrentlyEditedMessages.objects.filter(edited_message_id=edited_message_id).delete()

    response = {

        "response_text": "Edited Messages Table has been Emptied!"

    }

    return JsonResponse(response, safe=False)

from django.db import models

from django.contrib.auth.models import User
from Registration_Login_App.models import Profile

# Create your models here.


class ChatRoom(models.Model):
    room_title = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, blank=True)
    is_two_user_chat = models.BooleanField(default=True)
    creation_time = models.DateTimeField(auto_now_add=True)


class ChatMessage(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, default="")

    message_text = models.TextField(blank=False)
    message_sender = models.ForeignKey(User, on_delete=models.CASCADE)

    is_message_edited = models.BooleanField(default=False)

    creation_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message_text + " - " + self.message_sender.username + " to chatroom " + str(self.chatroom.id)


class CurrentlyDeletedMessages(models.Model):

    deleted_message_id = models.IntegerField()

    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)

    message_sender = models.ForeignKey(User, on_delete=models.CASCADE)


class CurrentlyEditedMessages(models.Model):

    edited_message_id = models.IntegerField()

    edited_message_text = models.TextField(blank=False)

    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)

    message_editor = models.ForeignKey(User, on_delete=models.CASCADE)


from django.urls import path

from . import views

urlpatterns = [
    path('MyChats/', views.chats_main, name="chats-main-page"),
    path('create_chat/<int:user_pk>', views.create_chat, name="create-chat"),
    path('chatroom/<int:chat_pk>', views.show_chat, name="show-chat"),
    path('send_message/', views.send_message, name="send-message"),
    path('delete_message/', views.delete_message, name="delete-message"),
    path('edit_message/', views.edit_message, name="edit-message"),
    path('check_for_new_messages/', views.check_for_new_messages, name="check-for-new-messages"),
    path('empty_deleted_messages_table/', views.empty_deleted_messages_table, name="empty-deleted-messages-table"),
    path('empty_edited_messages_table/', views.empty_edited_messages_table, name="empty-edited-messages-table"),

]

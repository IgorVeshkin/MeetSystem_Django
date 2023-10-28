from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name="main-page"),
    path('show-meeting/<int:meeting_pk>', views.show_meeting, name="show-meeting"),
    path('testing_page/', views.test, name="testing_page"),
    path('create_meeting/', views.create_meeting_form, name="create_meeting"),
    path('delete_meeting/<int:meeting_pk>', views.delete_meeting, name="delete-meeting"),
    path('create_event/', views.create_event_form, name="create_event"),
    path('edit_event/<int:event_pk>', views.edit_event_form, name="edit_event"),
    path('add_event_to_profile/<int:event_pk>', views.add_event_to_profile, name="add-event-to-profile"),
    path('remove_event_from_profile/<int:event_pk>', views.remove_event_from_profile, name="remove-event-from-profile"),
    path('profile/<int:user_pk>', views.show_profile, name="show-profile"),
    path('profile-settings/<int:user_pk>', views.profile_settings, name="profile-settings"),
    path('get_day_schedule_for_event_form/', views.get_day_schedule_for_event_form, name='get-day-schedule-for-event-form'),
    path('get_start_time_check_for_event_form/', views.get_start_time_check_for_event_form, name='get-start-time-check-for-event-form'),
    path('delete_event/<int:event_pk>', views.delete_event, name="delete-event"),
    path('check_current_event_in_profile/', views.check_current_event_in_profile, name='check-current-event-in-profile'),
    path('show_users_list/', views.show_users_list, name="show-users-list"),
    path('get_user_by_id_in_search_page/', views.get_user_by_id_in_search_page, name='get-user-by-id-in-search-page'),
    path('get_user_by_nickname_role_in_search_page/', views.get_user_by_nickname_role_in_search_page, name='get-user-by-nickname-role-in-search-page'),
    path('ban_user/<int:user_pk>', views.ban_user, name="ban-user"),
    path('unban_user/<int:user_pk>', views.unban_user, name="unban-user"),
    path('about/', views.about_site, name="about-site"),
]

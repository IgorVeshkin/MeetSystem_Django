from datetime import datetime

import datetime as dt

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from Registration_Login_App.forms import EditUserForm
from .models import Meeting, Event

from Registration_Login_App.models import Profile, User

from functools import wraps

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


# Create your views here.


# Decorators for page opening restrictions

def logged_user_required(view_function):

    @wraps(view_function)
    def inner_function(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("main-page")

        return view_function(request, *args, **kwargs)

    return inner_function

# https://stackoverflow.com/questions/5469159/how-to-create-a-custom-decorator-in-django


def admin_required(view_function): #, redirect_page_name="main-page"):
    @wraps(view_function)
    def inner_function(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("main-page")

        else:
            if request.user.profile.role != "Admin":
                return redirect("main-page")
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        return view_function(request, *args, **kwargs)

    return inner_function


def main(request):

    context = {
        "Meetings": Meeting.objects.all()
    }

    # print('Event.profile_set', Event.objects.filter(pk=1)[0].profile_set.all().count())
    # print('Meeting.profile_set', Meeting.event_set.all())

    return render(request, "MeetingSystem_CRUD/Event_Schedule_App_Meeting_Display_page.html", context=context)


def show_meeting(request, meeting_pk):

    events_of_the_meeting = Meeting.objects.get(pk=meeting_pk) # Event.objects.filter()

    current_meeting = Meeting.objects.get(pk=meeting_pk)

    # print('events_of_the_meeting', events_of_the_meeting)

    events_of_the_meeting = events_of_the_meeting.event_set.all().order_by('event_date', 'event_start_time') #.order_by("event_start_time")

    print("events_of_the_meeting", events_of_the_meeting)

    # print('events_of_the_meeting 2', events_of_the_meeting)

    # print("meeting_pk", meeting_pk)

    context = {
        "Events_of_the_meeting": events_of_the_meeting,
        "Current_Meeting": current_meeting,
               }

    # dates_and_items = {}
    #
    # for event in events_of_the_meeting:
    #     current_key = event.display_date.date()  # the item's date
    #     dates_and_items.setdefault(current_key, []).append(event)
    #
    # context['dates_items'] = dates_and_items

    # print("events_of_the_meeting", events_of_the_meeting, meeting_pk, type(events_of_the_meeting))

    return render(request, "MeetingSystem_CRUD/Event_Schedule_App_Show_Meeting_Schedule.html", context=context)


def test(request):
    return render(request, "MeetingSystem_CRUD/Chats_base_template.html", context={})


@admin_required
def create_meeting_form(request):
    if request.method == "GET":
        if "meeting-title" in request.GET:
            new_meeting = Meeting(meeting_title=request.GET["meeting-title"],
                                  meeting_description=request.GET["meeting-description"],
                                  company_name=request.GET["company-name"],
                                  start_date=request.GET["meeting-start-date"],
                                  end_date=request.GET["meeting-end-date"])

            new_meeting.save()

            return redirect("create_meeting")

    return render(request, "MeetingSystem_CRUD/Event_Schedule_App_Create_Meeting_page.html", context={})


@admin_required
def create_event_form(request):

    if request.method == "GET":
        if "meeting-event-title" in request.GET:

            print('start time created =', request.GET["form-meeting-event-start-time-input"], request.GET["form-meeting-event-end-time-input"], type(request.GET["form-meeting-event-start-time-input"]))

            meeting_record = Meeting.objects.filter(pk=request.GET["meeting-select"])

            print("MeetingRecord", meeting_record[0])

            print("Request GET", request.GET)

            event_start_time = datetime.strptime(request.GET["form-meeting-event-start-time-input"], '%H:%M').time()
            event_end_time = datetime.strptime(request.GET["form-meeting-event-end-time-input"], '%H:%M').time()

            print('111111', event_start_time)

            new_event = Event(event_title=request.GET["meeting-event-title"],
                              event_description=request.GET["event-description"],
                              meeting=meeting_record[0],
                              event_date=request.GET["form-meeting-event-end-date-input"],
                              event_start_time=event_start_time,
                              event_end_time=event_end_time
                              )

            new_event.save()

            return redirect("create_event")

    meeting_records = Meeting.objects.all()

    events_of_the_meeting = Meeting.objects.get(pk=meeting_records[0].pk)
    events_of_the_meeting = events_of_the_meeting.event_set.order_by('event_date', 'event_start_time') #.order_by("event_start_time")

    context = {
        "Meetings": meeting_records,
        "Start_End_Dates": zip(Meeting.objects.values("pk"), Meeting.objects.values("start_date"), Meeting.objects.values("end_date")),
        "Events_of_the_meeting": events_of_the_meeting,
               }
    return render(request, "MeetingSystem_CRUD/Event_Schedule_App_Create_Event_page.html", context=context)


@admin_required
def edit_event_form(request, event_pk):

    event_record = Event.objects.get(pk=int(event_pk))

    if request.method == "GET":

        if "meeting-event-title" in request.GET:

            event_start_time = request.GET["form-meeting-event-start-time-input"]
            event_end_time = request.GET["form-meeting-event-end-time-input"]

            print("!!!!!!!!!!!", len(event_start_time), len(event_end_time))
            print('start time =', request.GET["form-meeting-event-start-time-input"], request.GET["form-meeting-event-end-time-input"], type(request.GET["form-meeting-event-start-time-input"]))

            if len(event_start_time) == 8:
                event_start_time = datetime.strptime(request.GET["form-meeting-event-start-time-input"], '%H:%M:%S').time()
                print('dgdgs', event_start_time)
                event_end_time = datetime.strptime(request.GET["form-meeting-event-end-time-input"], '%H:%M:%S').time()
            elif len(event_start_time) == 5:
                event_start_time = datetime.strptime(str(request.GET["form-meeting-event-start-time-input"]) + ":00",
                                                     '%H:%M:%S').time()
                print('dgdgs', event_start_time)
                event_end_time = datetime.strptime(str(request.GET["form-meeting-event-end-time-input"]) + ":00",
                                                   '%H:%M:%S').time()

            event_record.event_title = request.GET.get('meeting-event-title')
            event_record.event_description = request.GET.get('event-description')
            event_record.meeting = Meeting.objects.filter(pk=request.GET["meeting-select"])[0]
            event_record.event_date = request.GET.get('form-meeting-event-end-date-input')
            event_record.event_start_time = event_start_time
            event_record.event_end_time = event_end_time

            event_record.save()

            return redirect("edit_event", event_pk)

    # event_record = Event.objects.get(pk=int(event_pk))

    meeting_records = Meeting.objects.all()

    events_of_the_meeting = Meeting.objects.get(pk=meeting_records[0].pk)
    events_of_the_meeting = events_of_the_meeting.event_set.order_by('event_date', 'event_start_time')

    print('event_record =', event_record, event_pk)

    context = {
        "Meetings": meeting_records,
        "Start_End_Dates": zip(Meeting.objects.values("pk"), Meeting.objects.values("start_date"),
                               Meeting.objects.values("end_date")),
        "Events_of_the_meeting": events_of_the_meeting,
        "event_record_for_edit": event_record,

    }

    return render(request, "MeetingSystem_CRUD/Event_Schedule_App_Edit_Event_page.html", context=context)


def get_day_schedule_for_event_form(request):
    """"""

    meeting_pk = request.GET.get('meeting-select', None)

    event_date = request.GET.get('form-meeting-event-end-date-input', None)

    meeting_record = Meeting.objects.get(pk=meeting_pk)
    events_of_this_day = meeting_record.event_set.all().filter(event_date=event_date).order_by("event_start_time")

    print(list(events_of_this_day.values("event_title", "event_start_time", "event_end_time")))

    response = {
        'events_of_the_day': list(events_of_this_day.values()),
        'todays_date': event_date,
    }

    return JsonResponse(response, safe=False)


def get_start_time_check_for_event_form(request):

    meeting_pk = request.GET.get('meeting-select', None)

    event_date = request.GET.get('form-meeting-event-end-date-input', None)

    current_start_time = request.GET.get('event-time', None)

    print("current start time", current_start_time)

    meeting_record = Meeting.objects.get(pk=meeting_pk)
    events_of_this_day = meeting_record.event_set.all().filter(event_date=event_date).order_by("event_start_time")

    time_periods = events_of_this_day.values("event_start_time", "event_end_time")

    print("time_periods", time_periods.all())

    start_time_mistake = False

    for start_time in time_periods.all():
        print("151234", start_time)
        if start_time.get("event_start_time") < dt.time.fromisoformat(current_start_time) < start_time.get("event_end_time"):
            start_time_mistake = True
            break
        else:
            start_time_mistake = False

    response = {
        'time_mistake': start_time_mistake,

    }

    return JsonResponse(response, safe=False)


def add_event_to_profile(request, event_pk):
    event_to_add = Event.objects.get(id=event_pk)
    user_profile = Profile.objects.get(user=request.user)
    user_profile.user_events.add(event_to_add)

    return redirect(request.META.get('HTTP_REFERER'))


def remove_event_from_profile(request, event_pk):
    event_to_remove = Event.objects.get(id=event_pk)
    user_profile = Profile.objects.get(user=request.user)
    user_profile.user_events.remove(event_to_remove)

    return redirect(request.META.get('HTTP_REFERER'))


def delete_event(request, event_pk):
    event_to_remove = Event.objects.get(id=event_pk)
    event_to_remove.delete()

    return redirect(request.META.get('HTTP_REFERER'))


@logged_user_required
def show_profile(request, user_pk):

    if request.user.pk == user_pk:
        current_user = request.user
        events_of_the_user = current_user.profile.user_events.all().order_by('event_date', "event_start_time")#.order_by("event_start_time")
    else:
        current_user = User.objects.get(pk=user_pk)
        events_of_the_user = current_user.profile.user_events.all().order_by('event_date', "event_start_time")

    # request.user.profile.user_events.all()

    print('events_of_the_user', events_of_the_user)

    context = {
        "Events_of_the_user": events_of_the_user,
        "Current_User": current_user,
    }

    return render(request, "MeetingSystem_CRUD/Event_Schedule_App_User_Profile_page.html", context=context)


@logged_user_required
def profile_settings(request, user_pk):
    if request.user.pk != user_pk:
        return redirect('/')

    if request.method == "POST":
        print('value in profile settings on change', request.POST.get('hide-user-profile-on-search-page'))

        edit_user_form = EditUserForm(request.POST, instance=request.user)

        if edit_user_form.is_valid():
            edit_user_form.save()

        hide_profile_or_not =request.POST.get('hide-user-profile-on-search-page')

        # print('gfgd', True if hide_profile_or_not == 'on' else False)

        request.user.profile.is_hidden_on_search_page = True if hide_profile_or_not == 'on' else False
        request.user.profile.save()

    context = {
        "EditUserForm": EditUserForm(instance=request.user)
    }

    return render(request, "MeetingSystem_CRUD/Event_Schedule_App_Profile_Settings.html", context=context)


@logged_user_required
def show_users_list(request):

    if request.user.is_authenticated and request.user.profile.role == "Admin":
        SystemUsers = User.objects.all()
    else:
        SystemUsers = User.objects.filter(profile__is_hidden_on_search_page=False, profile__is_banned=False)

    context = {
        "SystemUsers": SystemUsers,

    }

    return render(request, "MeetingSystem_CRUD/Event_Schedule_App_Show_Users_List_Page.html", context=context)


def get_user_by_id_in_search_page(request):

    user_pk = request.GET.get('user_pk', None)

    if request.user.is_authenticated and request.user.profile.role == "Admin":
        found_user = list(User.objects.filter(pk=user_pk).values())
        found_user_profile = list(Profile.objects.filter(user=user_pk).values())
    else:
        found_user = list(User.objects.filter(pk=user_pk, profile__is_hidden_on_search_page=False, profile__is_banned=False).values())
        found_user_profile = list(Profile.objects.filter(user=user_pk, is_hidden_on_search_page=False, is_banned=False).values())

    response = {
        'found_user': found_user,
        'found_user_profile': found_user_profile,

    }

    return JsonResponse(response, safe=False)


def get_user_by_nickname_role_in_search_page(request):

    username = request.GET.get('username', None)

    role = request.GET.get('role', None)

    print('username', username)

    print("User icontains", User.objects.filter(username__icontains=username).values())

    if role == "All":

        if request.user.profile.role == "Admin":
            Found_Users = User.objects.filter(username__icontains=username)

            Profiles = Profile.objects.filter(user__in=Found_Users.values("id"))

        else:
            Found_Users = User.objects.filter(username__icontains=username, profile__is_hidden_on_search_page=False, profile__is_banned=False)

            Profiles = Profile.objects.filter(user__in=Found_Users.values("id"))

    else:

        if request.user.profile.role == "Admin":

            Profiles = Profile.objects.filter(role=role)

            print('Profiles values', Profiles.values("user_id"))

            Found_Users = User.objects.filter(id__in=Profiles.values("user_id")).filter(username__icontains=username)

        else:

            Profiles = Profile.objects.filter(role=role, is_hidden_on_search_page=False, is_banned=False)

            print('Profiles values', Profiles.values("user_id"))

            Found_Users = User.objects.filter(id__in=Profiles.values("user_id")).filter(username__icontains=username)

    print("Profiles", Profiles)

    response = {
        'found_users': list(Found_Users.values()),
        'found_users_profiles': list(Profiles.values()),
        # 'found_users_ids': list(Found_Users.values("id")),
        # 'found_user_profile': list(Profile.objects.filter(user_username__icontains=username).values()),

    }

    return JsonResponse(response, safe=False)


def check_current_event_in_profile(request):
    user_pk_to_check_in_profile = request.GET.get("event-pk-to-check-in-profile", None)

    # print('user_pk_to_check_in_profile', user_pk_to_check_in_profile, type(user_pk_to_check_in_profile))

    is_event_in_current_profile = request.user.profile.user_events.all().filter(id=int(user_pk_to_check_in_profile)).exists()

    print('gdgdggd', request.user.profile.user_events.all().filter(id=int(user_pk_to_check_in_profile)).exists()) #.get(user_events=int(user_pk_to_check_in_profile)).exists())

    # if int(user_pk_to_check_in_profile) in request.user.profile.user_events.all().values('id')[0]:
    #     print('works')
    # else:
    #     print('does not work')

    response = {
        "is_event_in_current_profile": is_event_in_current_profile,
    }

    return JsonResponse(response, safe=False)


def ban_user(request, user_pk):
    User_to_ban = User.objects.get(id=user_pk)

    User_to_ban.profile.is_banned = True

    User_to_ban.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def unban_user(request, user_pk):
    User_to_unban = User.objects.get(id=user_pk)

    User_to_unban.profile.is_banned = False

    User_to_unban.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def about_site(request):

    return render(request, "MeetingSystem_CRUD/Event_Schedule_App_About_Site.html", context={})


def delete_meeting(request, meeting_pk):

    Meeting.objects.get(id=int(meeting_pk)).delete()

    return redirect("main-page")


def handling_404_page(request, exception):

    return render(request, "404_page.html", context={})


# @receiver(user_logged_in)
# def got_online(sender, user, request, **kwargs):
#     user.profile.is_online = True
#     user.profile.save()
#
#
# @receiver(user_logged_out)
# def got_offline(sender, user, request, **kwargs):
#     user.profile.is_online = False
#     user.profile.save()

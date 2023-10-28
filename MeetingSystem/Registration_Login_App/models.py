from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from MeetingSystem_CRUD.models import Event
from django.db import models

# Create your models here.


class Profile(models.Model):
    Admin_role_title = "Admin"
    User_role_title = "User"

    role_choices = [
        (Admin_role_title, "Admin"),
        (User_role_title, "User")
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=5, blank=False, choices=role_choices, default="User")
    user_events = models.ManyToManyField(Event, blank=True)
    is_hidden_on_search_page = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return f"Профиль: {self.user.username} - {self.role}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

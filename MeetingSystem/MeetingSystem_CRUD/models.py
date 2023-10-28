from django.db import models

# Create your models here.


class Meeting(models.Model):
    meeting_title = models.CharField(max_length=255)
    meeting_description = models.TextField(blank=False)
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    creation_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.meeting_title


class Event(models.Model):
    event_title = models.CharField(max_length=255)
    event_description = models.TextField(blank=False)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=False)
    event_date = models.DateField()
    event_start_time = models.TimeField()
    event_end_time = models.TimeField()

    creation_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_title

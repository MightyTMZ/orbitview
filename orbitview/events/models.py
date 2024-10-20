from django.db import models
from ckeditor.fields import RichTextField

"""
Purpose: Manages webinars, workshops, and other events hosted on the platform.

Features:
- Event creation and management
- Event registration for users
- Calendar integration
- Real-time webinars with integrations (Zoom, Google Meet)
- Notifications and reminders
"""

class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    """location_url1 = models.CharField(max_length=2083) # e.g. you have a Google Maps link
    location_url2 = models.CharField(max_length=2083, null=True, blank=True) # e.g. you have a IOS Maps link
    location_url3 = models.CharField(max_length=2083, null=True, blank=True) # e.g. you have a Google Maps link"""
    description = RichTextField()

    def __str__(self) -> str:
        return f"{self.title} - {self.date.date()}"


class Location(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=2083)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="locations")

    

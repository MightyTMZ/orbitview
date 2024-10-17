from django.db import models
from django.conf import settings
import secrets


"""
Purpose: Handles user interaction within the platform, including networking, messaging, and engagement with content.

Features:
- Messaging system (private and group)
- Notifications
- User-to-user connections (follow, like, etc.)
- Interaction with posts (likes, shares, comments)
- AI-driven content recommendations
"""


def generate_random_code():
    return secrets.randbelow(10**16)  # Generates a random 16-digit number


class MessageChat(models.Model):
    unique_code = models.CharField(max_length=16, unique=True, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='group_chats', blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(generate_random_code())
        super().save(*args, **kwargs)


    def __str__(self) -> str:
        return self.code



class Message(models.Model):
    chat = models.ForeignKey(MessageChat, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=1500) # in the future, we can turn this into a rich text field where it allows users to send images too






# group chats should i have members, how do i do that without causing the apps to be dependent on each other
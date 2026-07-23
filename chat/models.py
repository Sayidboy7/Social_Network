from django.conf import settings
from django.db import models
from auth_network.models import User

from django.utils import timezone


class Conversation(models.Model):
    class StatusChoices(models.TextChoices):
        PRIVATE = ('PRIVATE', 'Private')
        GROUP = ('GROUP', 'Group')

    participants = models.ManyToManyField(
        User,
        related_name="conversations"
    )

    status = models.CharField(max_length=8, choices=StatusChoices.choices)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Conversation {self.pk}"

    def has_participant(self, user):
        return self.participants.filter(pk=user.pk).exists()

    @property
    def last_message(self):
        return self.messages.order_by('-created_at').first().body if self.messages.order_by('-created_at').first() else 'None'

    def other_user(self, current_user_id):
        return self.participants.exclude(id=current_user_id).first()


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )

    body = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    is_seen = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender} - {self.body[:30]}"


    
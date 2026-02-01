from django.core.validators import MinLengthValidator
from django.db import models


class Chat(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id}: {self.title}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    text = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Msg {self.id} in Chat {self.chat_id}"


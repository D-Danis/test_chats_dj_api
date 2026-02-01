import logging

from rest_framework import serializers

from .models import Chat, Message

logger = logging.getLogger('serializers')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "chat_id", "text", "created_at"]
        read_only_fields = ["id", "chat_id", "created_at"]
    
    def validate_text(self, value):
        value = value.strip()
        if not (1 <= len(value) <= 5000):
            logger.error("ValidationError: text length must be 1..5000")
            raise serializers.ValidationError("text length must be 1..5000")
        return value


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Chat
        fields = ["id", "title", "created_at", "messages"]

    def validate_title(self, value):
        value = value.strip()
        if not (1 <= len(value) <= 200):
            logger.error("ValidationError: text length must be 1..200")
            raise serializers.ValidationError("title length must be 1..200")
        return value

    


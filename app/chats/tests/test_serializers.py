from django.test import TestCase

from chats.models import Chat, Message
from chats.serializers import ChatSerializer, MessageSerializer


class ChatApiTestCase(TestCase):
    def test_chat(self):
        chat_1 = Chat.objects.create(title="Test Chat_1")
        chat_2 = Chat.objects.create(title="Test Chat_2")
        message = Message.objects.create(chat=chat_1, text="Test Message 1")
        chats = Chat.objects.all()
        serializer_data = ChatSerializer(chats, many=True).data
        expected_data = [
            {
                "id": chat_1.id,
                "title": "Test Chat_1",
                "created_at": chat_1.created_at,
                "messages": [
                                {
                                    "id": message.id , 
                                    "chat_id": message.chat.id, 
                                    "text": "Test Message 1", 
                                    "created_at": message.created_at
                                }
                        ]
             },
            {
                "id": chat_2.id,
                "title": "Test Chat_2",
                "created_at": chat_2.created_at,
                "messages": []
             }
        ]
        self.assertEqual(expected_data, serializer_data)
    
    def test_chat_not_create(self):
        serializer = ChatSerializer(data={"title": ""})
        assert not serializer.is_valid()
        assert "title" in serializer.errors


class MessageApiTestCase(TestCase):
    def test_message(self):
        chat_1 = Chat.objects.create(title="Test Chat_1")
        message_1 = Message.objects.create(chat=chat_1, text="Test Message 1")
        message_2 = Message.objects.create(chat=chat_1, text="Test Message 2")
        message = Message.objects.all()
        serializer_data = MessageSerializer(message, many=True).data
        expected_data = [
            {
                'id': message_1.id, 
                'chat_id': chat_1.id, 
                'text': 'Test Message 1', 
                'created_at':  message_1.created_at
            }, 
            {
                'id': message_2.id, 
                'chat_id': chat_1.id, 
                'text': 'Test Message 2', 
                'created_at': message_2.created_at
            }
        ]
        self.assertEqual(expected_data, serializer_data)
        
    def test_message_not_create(self):
        chat_1 = Chat.objects.create(title="Test Chat_1")
        serializer = ChatSerializer(data={'chat_id': chat_1.id, "text": ""})
        assert not serializer.is_valid()
        
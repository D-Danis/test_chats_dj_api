import json

from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from chats.models import Chat, Message
from chats.serializers import MessageSerializer


class MessageAPITestCase(APITestCase):
    def setUp(self):
        self.chat = Chat.objects.create(title="Test Chat_1")
        self.message_1 = Message.objects.create(chat=self.chat, text="Test Message 1")
        self.message_2 = Message.objects.create(chat=self.chat, text="Test Message 2")
    
    def test_get(self):
        url = reverse('chat-messages-list', kwargs={'chat_pk': self.chat.pk})
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
        messages = Message.objects.filter(chat_id=self.chat.id).order_by("created_at")
        serializer_data =  MessageSerializer(messages,many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
    
    def test_get_detail(self):
        url = reverse('chat-messages-detail', kwargs={'chat_pk': self.chat.pk, 'pk': self.message_1.pk})
        response = self.client.get(url)
        messages = Message.objects.get(chat_id=self.chat.pk, id=self.message_1.pk)
        serializer_data =  MessageSerializer(messages).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        
    def test_create(self):
        self.assertEqual(2, Message.objects.filter(chat_id=self.chat.id).count())
        url = reverse('chat-messages-list', kwargs={'chat_pk': self.chat.pk})
        data = {
                "text": "Test Text 3",
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Message.objects.filter(chat_id=self.chat.id).count())
        
    def test_update(self):
        url = reverse('chat-messages-detail', kwargs={'chat_pk': self.chat.pk, 'pk': self.message_1.pk})
        data = {
                "text": "Test Text New",
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)
        self.message_1.refresh_from_db()
        self.assertEqual("Test Text New", self.message_1.text)
    
    def test_delete(self):
        self.assertEqual(2, Message.objects.filter(chat_id=self.chat.id).count())
        url = reverse('chat-messages-detail', kwargs={'chat_pk': self.chat.pk, 'pk': self.message_2.pk})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Message.objects.filter(chat_id=self.chat.id).count())
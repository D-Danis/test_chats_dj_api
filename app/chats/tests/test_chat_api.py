import json
import logging

from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from chats.models import Chat, Message
from chats.serializers import ChatSerializer

logger = logging.getLogger('serializers')


class ChatAPITestCase(APITestCase):
    def setUp(self):
        self.chat_1 = Chat.objects.create(title="Test Chat_1")
        self.chat_2 = Chat.objects.create(title="Test Chat_2")
        self.message = Message.objects.create(chat=self.chat_1, text="Test Message 1")
    
    def test_get(self):
        logger.info("Test Get")
        url = reverse('chat-list')
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
        chats = Chat.objects.all().prefetch_related('messages')
        serializer_data = ChatSerializer(chats,many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        logger.info("Status Code: HTTP 200 OK")
        self.assertEqual(serializer_data, response.data)
    
    def test_get_detail(self):
        logger.info("Test Get Detail")
        url = reverse('chat-detail', args=(self.chat_1.id,))
        response = self.client.get(url)
        books = Chat.objects.get(id=self.chat_1.id)
        serializer_data = ChatSerializer(books).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        logger.info("Status Code: HTTP 200 OK")
        self.assertEqual(serializer_data, response.data)
        
    def test_create(self):
        logger.info("Test Create")
        logger.info("Count obj: 2")
        self.assertEqual(2, Chat.objects.all().count())
        url = reverse('chat-list')
        data = {
                "title": "Test 3",
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        logger.info("Status Code: HTTP 201 CREATED")
        self.assertEqual(3, Chat.objects.all().count())
        logger.info("Count obj: 3")
        
    def test_update(self):
        logger.info("Test Update")
        url = reverse('chat-detail', args=(self.chat_1.id,))
        data = {
                "title": "Test New",
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        logger.info("Status Code: HTTP 200 OK")
        self.chat_1.refresh_from_db()
        self.assertEqual("Test New", self.chat_1.title)
        logger.info("Update title")
    
    def test_delete(self):
        logger.info("Test Delete")
        self.assertEqual(2, Chat.objects.all().count())
        logger.info("Count obj: 2")
        url = reverse('chat-detail', args=(self.chat_2.id,))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        logger.info("Status Code: HTTP 204 NO CONTENT")
        self.assertEqual(1, Chat.objects.all().count())
        logger.info("Count obj: 1")
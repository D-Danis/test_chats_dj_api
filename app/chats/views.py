from rest_framework.viewsets import ModelViewSet

from chats.models import Chat, Message
from chats.serializers import ChatSerializer, MessageSerializer


class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all().prefetch_related('messages')
    serializer_class = ChatSerializer


class MessagesViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    
    def perform_create(self, serializer):
        chat_pk = self.kwargs.get('chat_pk') or self.kwargs.get('pk')
        serializer.save(chat_id=chat_pk)
        
    def get_queryset(self):
        chat_pk = self.kwargs.get("chat_pk") or self.kwargs.get("pk")
        if chat_pk:
            return Message.objects.filter(chat_id=chat_pk).order_by("created_at")
        return Message.objects.none()  